from django.urls import re_path as url

from games.views import GameAutocomplete

app_name = "games"

urlpatterns = [
    url(
        r"^game-autocomplete/$",
        GameAutocomplete.as_view(),
        name="game-autocomplete",
    ),
]
