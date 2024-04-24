from django.conf import settings
from django.db import models


class GameStat(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    top_5_hours = models.JSONField(default=list)
    top_5_last_2weeks = models.JSONField(default=list)
    favorite_game_name = models.CharField(max_length=255)
    favorite_game_url = models.URLField()
    favorite_game_playtime = models.IntegerField(default=0)

    def __str__(self):
        return f'Статистика {self.user.username}'

    @classmethod
    def create_or_update(
        cls, user, top_5_hours, top_5_last_2weeks, favorite_game,
    ):
        game_stat, created = cls.objects.get_or_create(user=user)
        game_stat.top_5_hours = [
            {'name': game.name, 'url': game.url, 'playtime': game.playtime}
            for game in top_5_hours
        ]
        game_stat.top_5_last_2weeks = [
            {'name': game.name, 'url': game.url, 'playtime': game.playtime}
            for game in top_5_last_2weeks
        ]
        game_stat.favorite_game_playtime = favorite_game.playtime
        game_stat.favorite_game_name = favorite_game.name
        game_stat.favorite_game_url = favorite_game.url
        game_stat.save()
