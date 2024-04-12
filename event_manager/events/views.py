from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View

from events.forms import AddParticipantForm, EventForm
from events.models import Event


class CreateEventView(CreateView):
    template_name = 'events/create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('homepage:home')


class AddParticipantView(View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)
            event.participants.add(user)
        return redirect(reverse('homepage:home'))


class RemoveParticipantView(View):
    def post(self, request):
        form = AddParticipantForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            user_id = form.cleaned_data['user_id']
            event = get_object_or_404(Event, id=event_id)
            user = get_object_or_404(get_user_model(), id=user_id)
            event.participants.remove(user)
        return redirect(reverse('homepage:home'))
