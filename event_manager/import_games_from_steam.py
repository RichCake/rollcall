import json

import requests

steam_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

response = requests.get(steam_url)
data = response.json()
out = []
for i, d in enumerate(data["applist"]["apps"]):
    out.append({"model": "games.game","pk": i + 1,"fields": {"name": d["name"]}})
with open("games_data.json", "w") as f:
    f.write(json.dumps(out))