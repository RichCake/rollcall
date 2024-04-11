from django.urls import reverse_lazy
from django.views.generic import CreateView

from events.forms import EventForm


class CreateEventView(CreateView):
    template_name = 'events/create_event.html'
    form_class = EventForm
    success_url = reverse_lazy('homepage:home')
