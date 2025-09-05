from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView
from events.models import Event, EventParticipants


class UserListView(ListView):
    template_name = "profiles/user_list.html"
    context_object_name = "users"
    model = get_user_model()


class UserDetailView(DetailView):
    template_name = "profiles/user_detail.html"
    context_object_name = "user"
    model = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object
        username = self.object.social_auth.filter(provider="telegram").first().extra_data["username"]
        context["tg_username"] = username[0] if isinstance(username, list) else username

        context["history"] = Event.objects.get_events_with_info(
            self.request.user,
        ).filter(eventparticipants__user=user, end__lt=timezone.now())
        context["created"] = Event.objects.get_events_with_info(
            self.request.user,
        ).filter(author=self.object)
        context["future"] = (
            Event.objects.get_events_with_info(self.request.user)
            .filter(
                eventparticipants__user=user,
                end__gte=timezone.now(),
                eventparticipants__status=EventParticipants.StatusChoices.REQUEST_ACCEPTED,
            )
            .order_by("end")
        )
        context["unanswered"] = Event.objects.get_events_with_info(
            self.request.user,
        ).filter(
            eventparticipants__user=user,
            eventparticipants__status=EventParticipants.StatusChoices.REQUEST_SENT,
        )
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profiles/user_update.html"
    context_object_name = "user"
    model = get_user_model()
    fields = ["username", "email", "avatar"]

    def get_success_url(self):
        return reverse_lazy("profiles:detail", args=[self.object.id])

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk != self.get_object().pk:
            raise Http404("Вы не имеете доступа к этой странице")
        return super().dispatch(request, *args, **kwargs)
