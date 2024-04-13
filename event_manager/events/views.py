from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import django.views.generic as views

from events.forms import AddParticipantForm, EventForm
from events.models import Event


class CreateEventView(views.CreateView):
    template_name = 'events/create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('homepage:home')


class UpdateEventView(views.UpdateView):
    template_name = 'events/update_event.html'
    model = Event
    fields = (
        Event.author.field.name,
        Event.title.field.name,
        Event.description.field.name,
        Event.end.field.name,
        Event.max_participants.field.name,
        Event.participants.field.name,
        Event.is_private.field.name,
    )
    queryset = (
        Event.objects
        .select_related('author')
        .prefetch_related('participants')
        .only(
            'title',
            'description',
            'max_participants',
            'author__username',
            'participants__username',
            )
        )

    def get_success_url(self):
        return reverse_lazy('events:update', args=[self.object.id])


class AddParticipantView(views.View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)
            if event.max_participants:
                if event.participants.count() >= event.max_participants:
                    return HttpResponseRedirect(
                        request.META.get('HTTP_REFERER'),
                        )
            event.participants.add(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveParticipantView(views.View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)
            event.participants.remove(user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class EventsListView(views.ListView):
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    queryset = (
        Event.objects
        .select_related('author')
        .prefetch_related('participants')
        .only(
            'title',
            'description',
            'max_participants',
            'author__username',
            'participants__username',
            )
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        author = self.request.GET.get('author')
        date = self.request.GET.get('date')
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
        if date:
            queryset = queryset.filter(end=date)
        return queryset


class DetailEventView(views.DetailView):
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    queryset = (
        Event.objects
        .select_related('author')
        .prefetch_related('participants')
        )
