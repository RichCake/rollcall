from django.urls import re_path as url

from games.views import GameAutocomplete

urlpatterns = [
    url(
        r'^game-autocomplete/$',
        GameAutocomplete.as_view(),
        name='game-autocomplete',
    ),
]