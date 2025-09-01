import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GB_API")
OUTPUT_FILE = "giantbomb_games.jsonl"
PROGRESS_FILE = "giantbomb_progress.txt"
LIMIT = 100
BASE_URL = "https://www.giantbomb.com/api/games/"


def get_last_offset():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_progress(offset):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(offset))


def fetch_page(offset, retries=5):
    params = {
        "api_key": API_KEY,
        "format": "json",
        "field_list": "name",
        "limit": LIMIT,
        "offset": offset,
    }
    headers = {
        "User-Agent": "RollCall/1.0"
    }
    for attempt in range(retries):
        try:
            response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("429 Too Many Requests, ждём 60 секунд...")
                time.sleep(60)
            else:
                print(f"Ошибка {response.status_code}, повтор через 5 секунд")
                time.sleep(5)
        except requests.RequestException as e:
            print(f"Ошибка сети: {e}, повтор через 5 секунд")
            time.sleep(5)
    raise RuntimeError(f"Не удалось загрузить offset={offset}")


def main():
    offset = get_last_offset()
    total = None
    i = offset

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        while True:
            data = fetch_page(offset)

            if total is None:
                total = data.get("number_of_total_results", 0)
                print(f"Всего игр: {total}")

            results = data.get("results", [])
            if not results:
                print("Больше данных нет.")
                break

            for game in results:
                i += 1
                record = {
                    "model": "games.game",
                    "pk": i,
                    "fields": {"name": game["name"]},
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

            print(f"Скачано {i}/{total}, offset={offset}")

            offset += LIMIT
            save_progress(offset)

            if offset >= total:
                print("Все страницы загружены.")
                break

            time.sleep(1)  # защита от бана


if __name__ == "__main__":
    main()
