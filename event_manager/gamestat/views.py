import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from gamestat.models import GameStat


class Game:
    def __init__(self, name, url, playtime):
        self.name = name
        self.url = url
        self.playtime = playtime

    def __str__(self):
        return f"{self.name}. Сыграно: {self.playtime}"


class SteamLoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(
            reverse("gamestat:steam_callback"),
        )
        return redirect(
            "https://steamcommunity.com/openid/login?openid.claimed_id="
            "http://specs.openid.net/auth/2.0/identifier_select&"
            "openid.identity=http://specs.openid.net/auth/2.0/"
            "identifier_select&openid.mode=checkid_setup&"
            "openid.ns=http://specs.openid.net/auth/2.0&openid.realm="
            f"{redirect_uri}&openid.return_to={redirect_uri}",
        )


class SteamCallbackView(View):
    def get(self, request):
        if "openid.identity" in request.GET:
            openid = request.GET["openid.identity"]
            steam_id = openid.split("/")[-1]
            user_data = requests.get(
                "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
                + settings.STEAM_API_KEY
                + "&steamid="
                + steam_id
                + "&format=json&include_appinfo=True&"
                "include_played_free_games=True",
            ).json()
            response = user_data["response"]
            top_5_hours = [
                Game(
                    i["name"],
                    f"https://store.steampowered.com/app/{i['appid']}",
                    int(i["playtime_forever"] / 60),
                )
                for i in sorted(
                    response["games"],
                    key=lambda x: -1 * x["playtime_forever"],
                )[:5]
            ]
            top_5_hours_last_week = [
                Game(
                    i["name"],
                    f"https://store.steampowered.com/app/{i['appid']}",
                    (0 if "playtime_2weeks" not in i else int(i["playtime_2weeks"] / 60)),
                )
                for i in sorted(
                    response["games"],
                    key=lambda x: (0 if "playtime_2weeks" not in x else -1 * x["playtime_2weeks"]),
                )[:5]
            ]
            favorite_game = top_5_hours[0]
            GameStat.create_or_update(
                user=request.user,
                top_5_hours=top_5_hours,
                top_5_last_2weeks=top_5_hours_last_week,
                favorite_game=favorite_game,
            )
            return redirect(reverse("gamestat:my_stats"))
        return HttpResponse("Вход через Steam не удался.")


class GameStatView(View):
    template_name = "gamestat/stats.html"

    def get(self, request):
        user = request.user
        try:
            game_stat = GameStat.objects.get(user=user)
        except GameStat.DoesNotExist:
            return HttpResponse(
                "Для данного пользователя нет статистики. Войдите в Steam.",
                status=404,
            )

        context = {"game_stat": game_stat}

        return render(request, self.template_name, context)
