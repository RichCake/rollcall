from django.contrib.auth import authenticate, forms, get_user_model
from django.db.models import Q


class SignUpForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "password1", "password2", "email"]


class ChangeForm(forms.UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("password")


class AuthEmailForm(forms.AuthenticationForm):
    def clean(self):
        user_model = get_user_model()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user_model = get_user_model()
        try:
            user = user_model.objects.get(
                Q(email=username) | Q(username=username),
            )
        except user_model.DoesNotExist:
            user = None

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=user.username if user else username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
