from django.urls import path

from gamestat import views

app_name = "gamestat"

urlpatterns = [
    path("steam/login/", views.SteamLoginView.as_view(), name="steam_login"),
    path(
        "steam/callback/",
        views.SteamCallbackView.as_view(),
        name="steam_callback",
    ),
    path("my-stats/", views.GameStatView.as_view(), name="my_stats"),
]
