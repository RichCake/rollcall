from django.contrib.auth import views
from django.urls import path, reverse_lazy

from users import forms
from users import views as users_views

app_name = 'users'

urlpatterns = [
    path(
        'activate/<int:userid>/',
        users_views.activate_view,
        name='activate',
    ),
    path('signup/', users_views.signup_view, name='signup'),
    path(
        'signup/done/',
        users_views.SignupSuccessView.as_view(),
        name='signup_success',
    ),
    path(
        'login/',
        views.LoginView.as_view(
            template_name='users/login.html',
            form_class=forms.AuthEmailForm,
        ),
        name='login',
    ),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logout.html'),
        name='logout',
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            success_url=reverse_lazy('users:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
