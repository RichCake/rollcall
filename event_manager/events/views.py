import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import Lower
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
import django.views.generic as views
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import datetime as dt

from events.forms import AddParticipantForm, AttendanceFormSet, EventForm
from events.models import Event, EventParticipants

logger = logging.getLogger(__name__)


class CreateEventView(LoginRequiredMixin, views.CreateView):
    template_name = 'events/create_event.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('events:detail', args=[self.object.id])

    def form_valid(self, form):
        event = form.save(commit=False)
        event.author = self.request.user
        event.save()
        self.object = event
        return FormMixin.form_valid(self, form)


class UpdateEventView(LoginRequiredMixin, views.UpdateView):
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
    

class DeleteEventView(LoginRequiredMixin, views.DeleteView):
    model = Event
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'


class AddParticipantView(LoginRequiredMixin, views.View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)

            if event.max_participants and event.participants.count() >= event.max_participants:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            event.participants.add(user)

            if user.telegram_chat_id:
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
                    args=json.dumps([30, event.title, user.telegram_chat_id]),
                )
        return HttpResponseRedirect(reverse_lazy('events:detail', args=[event.id]))


class RemoveParticipantView(LoginRequiredMixin, views.View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)
            event.participants.remove(user)
            PeriodicTask.objects.filter(name=f"Send notification to {user.id} for {event.id}").update(enabled=False)
        return HttpResponseRedirect(
            reverse_lazy('events:list'))


class EventsListView(views.ListView):
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12  # Показывать 12 событий на страницу
    queryset = (
        Event.objects
        .select_related('author', 'category')
        .prefetch_related('participants')
        .filter(is_private=False)
        .annotate(part_count=Count('eventparticipants'))
        .only(
            'category__name',
            'title',
            'description',
            'end',
            'author__username',
            'eventparticipants__user__username',
            'max_participants',
            )
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        author = self.request.GET.get('author')
        sort = self.request.GET.get('sort')
        if status:
            if status == 'status1':
                queryset = queryset.filter(participants=self.request.user)
            elif status == 'status2':
                queryset = queryset.exclude(participants=self.request.user)
        if author:
            if author == 'author1':
                queryset = queryset.filter(author=self.request.user)
            elif author == 'author2':
                queryset = queryset.exclude(author=self.request.user)
        if sort:
            if sort == 'end':
                queryset = queryset.order_by('-end')
            else:
                queryset = queryset.order_by(Lower(sort).asc())
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.request.GET.get('sort')
        return context


class DetailEventView(views.DetailView):
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    queryset = (
        Event.objects.get_public_events()
        .prefetch_related('eventparticipants_set')
        .only(
            'category__name',
            'title',
            'description',
            'created',
            'end',
            'is_private',
            'author__username',
            'eventparticipants__user__username',
            'eventparticipants__present',
            'max_participants',
            )
    )


def attendance_view(request, pk):
    event = get_object_or_404(Event, id=pk)
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
