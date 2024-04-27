import datetime as dt
import os

from django.core.management import BaseCommand
from django.utils import timezone
from dotenv import load_dotenv
import requests

from events.models import Event

load_dotenv()


class Command(BaseCommand):
    help = """Sends notifications to participants
     of an event that's coming up in an hour"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        coming_events = Event.objects.get_public_events().filter(
            end__gte=timezone.now(),
            end__lte=timezone.now() + dt.timedelta(hours=1),
            )
        for event in coming_events:
            minutes_to_event = (event.end - timezone.now()).seconds // 60
            participants = event.eventparticipants_set.filter(notified=False)
            for participant in participants:
                if participant.user.telegram_chat_id:
                    self.send_telegram_notification(participant.user.telegram_chat_id, event.title, minutes_to_event)
                else:
                    self.stdout.write(f"User {participant.user.username} is not linked to Telegram.")

                participant.notified = True
                participant.save()
        self.stdout.write('Notifications were sent.')

    def send_telegram_notification(self, chat_id, event_title, minutes_to_event):
        message = f'Через {minutes_to_event} минут будет {event_title}!'
        token = '6343049026:AAEQPW31DKskuXe-HYgpd_ZzIMgm3mseVtw'
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
        response = requests.get(url)
        self.stdout.write(str(response))
