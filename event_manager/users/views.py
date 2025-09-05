import datetime as dt

from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView

from users.forms import SignUpForm


def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("users:signup_success")

    return render(
        request,
        "users/signup.html",
        {"form": form},
    )


class SignupSuccessView(TemplateView):
    template_name = "users/signup_done.html"


def activate_view(request, userid):
    user = get_object_or_404(get_user_model(), pk=userid)
    twelve_hours = timezone.now() - dt.timedelta(hours=12)
    if not user.is_active:
        if user.date_joined > twelve_hours:
            user.is_active = True
            user.save()
            messages.success(request, "Вы активировали аккаунт. Можете войти!")
        else:
            messages.error(
                request,
                "Срок действия ссылки истек. Зарегиструруйтесь заново.",
            )
    else:
        messages.info(request, "Аккаунт уже активирован!")

    return render(request, "users/activate.html")


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.q:
            return get_user_model().objects.filter(
                username__icontains=self.q,
            )
        return get_user_model().objects.none()
