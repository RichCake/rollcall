import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
import django.views.generic as views
from django.views.generic.edit import FormMixin
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import datetime as dt
from django.http import Http404

from event_manager.celery import send_notification
from events.forms import ParticipantForm, AttendanceFormSet, EventForm, SearchEventForm
from events.models import Event, EventParticipants
from events.mixins import AuthorRequiredMixin

logger = logging.getLogger(__name__)


class CreateEventView(LoginRequiredMixin, views.CreateView):
    template_name = 'events/create_event.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('events:detail', args=[self.object.pk])

    def form_valid(self, form):
        event = form.save(commit=False)
        event.author = self.request.user
        event.save()
        self.object = event
        return FormMixin.form_valid(self, form)


class UpdateEventView(AuthorRequiredMixin, views.UpdateView):
    template_name = 'events/update_event.html'
    form_class = EventForm
    queryset = (
        Event.objects.get_public_events()
        .only(
            'category__name',
            'title',
            'description',
            'created',
            'end',
            'is_private',
            'author__username',
            'max_participants',
        )
    )

    def get_success_url(self):
        return reverse_lazy('events:update', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participants"] = (EventParticipants.objects
                                   .filter(event=self.object)
                                   .select_related("user"))
        return context


class DeleteEventView(AuthorRequiredMixin, views.DeleteView):
    model = Event
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'


class SendRequestView(LoginRequiredMixin, views.View):
    def post(self, request):
        form = ParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)

            accepted_participants = (EventParticipants.objects
                                     .filter(status=EventParticipants.StatusChoices.REQUEST_ACCEPTED,
                                             event=event)
                                     )
            if ((event.max_participants and accepted_participants.count() >= event.max_participants)
                    or event.participants.filter(eventparticipants__user=user).exists()):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            EventParticipants.objects.create(
                user=user,
                event=event,
                status=EventParticipants.StatusChoices.REQUEST_SENT,
            )
            social = event.author.social_auth.filter(provider="telegram").first()
            if social:
                text = f"Вам прислали заявку на событие {event.title}"
                send_notification.delay(text, social.uid)
            return HttpResponseRedirect(reverse_lazy('events:detail', args=[event.id]))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RevokeRequestView(LoginRequiredMixin, views.View):
    def post(self, request):
        form = ParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)

            EventParticipants.objects.filter(event__id=event_id, user__id=user_id).delete()
            PeriodicTask.objects.filter(name=f"Send notification to {user_id} for {event_id}").delete()
            social = user.social_auth.filter(provider="telegram").first()
            if social:
                text = f"Ваша заявка на событие {event.title} была удалена либо вами, либо организатором события"
                send_notification.delay(text, social.uid)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AcceptRequestView(LoginRequiredMixin, views.View):
    def post(self, request):
        form = ParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            if request.user == event.author:
                user = get_object_or_404(get_user_model(), id=user_id)
                part = EventParticipants.objects.filter(user=user, event=event).get()
                part.status = EventParticipants.StatusChoices.REQUEST_ACCEPTED
                part.save()

                social = user.social_auth.filter(provider="telegram").first()
                if social:
                    text = f"Вашу заявку на событие {event.title} приняли!"
                    send_notification.delay(text, social.uid)

                    schedule, created = IntervalSchedule.objects.get_or_create(
                        every=1,
                        period=IntervalSchedule.SECONDS,
                    )
                    PeriodicTask.objects.create(
                        interval=schedule,
                        name=f"Send notification to {user.id} for {event.id}",
                        start_time=event.end - dt.timedelta(minutes=30),
                        one_off=True,
                        task="event_manager.celery.send_notification",
                        args=json.dumps([f"Через 30 минут будет {event.title}!", social.uid]),
                    )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EventsListView(views.ListView):
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Event.objects
            .get_events_with_info(self.request.user)
            .filter(is_private=False)
        )
        title_contains = self.request.GET.get('title_contains')
        if title_contains:
            queryset = queryset.filter(title__icontains=title_contains)
        desc_contains = self.request.GET.get('desc_contains')
        if desc_contains:
            queryset = queryset.filter(description__icontains=desc_contains)
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author=author)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        game = self.request.GET.get('game')
        if game:
            queryset = queryset.filter(game=game)
        return queryset


class DetailEventView(LoginRequiredMixin, views.DetailView):
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    queryset = (
        Event.objects
        .select_related('author', 'category', 'game')
        .only(
            'category__name',
            'title',
            'description',
            'created',
            'end',
            'is_private',
            'author__id',
            'author__username',
            'max_participants',
            'game__name',
        )
    )

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        participants = (EventParticipants.objects
                                  .select_related("user")
                                  .filter(event__id=self.object.id)
                                  .only("present", "user__username", "user__id")).all()
        accepted_participants = participants.filter(status=EventParticipants.StatusChoices.REQUEST_ACCEPTED)
        contex["participants"] = accepted_participants[:5]
        contex["part_count"] = accepted_participants.count()
        contex["is_sent_request"] = (participants
                                     .filter(user=self.request.user)
                                     .exists())
        return contex


class ControlPanelEventView(views.DetailView):
    template_name = 'events/control_panel.html'
    context_object_name = 'event'
    queryset = (
        Event.objects
        .select_related('author', 'category')
    )

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        participants = (EventParticipants.objects
                                  .select_related("user")
                                  .filter(event__id=self.object.id)
                                  .only("present", "user__username", "user__id")).all()
        accepted_participants = participants.filter(status=EventParticipants.StatusChoices.REQUEST_ACCEPTED)
        contex["participants"] = accepted_participants
        contex["part_count"] = accepted_participants.count()
        return contex


class EventParticipantsListView(views.ListView):
    template_name = "events/participants_list.html"
    context_object_name = "participants"
    queryset = EventParticipants.objects.select_related("user")
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        queryset = queryset.filter(event__pk=pk)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        pk = self.kwargs.get("pk")
        context["event"] = Event.objects.filter(pk=pk).only("title", "id").get()
        return context


def attendance_view(request, pk):
    event = get_object_or_404(Event, id=pk)
    if request.user.pk != event.author.pk:
        raise Http404()
    formset = AttendanceFormSet(
        request.POST or None,
        queryset=EventParticipants.objects.filter(event__id=pk),
    )

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect("events:detail", pk=pk)

    return render(
        request,
        'events/attendance.html',
        {'event': event, 'formset': formset},
    )


class SearchEventView(views.FormView):
    template_name = "events/search_event.html"
    form_class = SearchEventForm
    success_url = reverse_lazy("events:list")
