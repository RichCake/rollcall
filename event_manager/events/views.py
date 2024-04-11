from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from events.models import Event

from events.forms import EventForm, AddParticipantForm


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
            print("DEBUG", 1)
            user = get_object_or_404(User, id=user_id)
            print("DEBUG", 2)
            event.participants.add(user)
            return redirect(reverse('homepage:home'))
