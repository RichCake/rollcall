from django.views.generic import ListView

from events.models import Event


class HomeView(ListView):
    template_name = 'homepage/main.html'
    context_object_name = 'events'
    queryset = Event.objects.all()
