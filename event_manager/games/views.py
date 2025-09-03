from dal import autocomplete
from django.contrib.postgres.search import TrigramSimilarity

from games.models import Game


class GameAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if self.q:
            queryset = (
                Game.objects
                .filter(name__trigram_similar=self.q)
                .annotate(similarity=TrigramSimilarity("name", self.q))
                .order_by("-similarity")
            )
            return queryset
        return Game.objects.none()