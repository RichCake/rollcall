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
            # participants = event.eventparticipants_set.filter(notified=False)
            for user in event.participants.all():
                if user.telegram_chat_id:
                    self.send_telegram_notification(user.telegram_chat_id, event.title, minutes_to_event)
                else:
                    self.stdout.write(f"User {user.username} is not linked to Telegram.")

                # participant.notified = True
                # user.save()
        self.stdout.write('E-mail Report was sent.')

    def send_telegram_notification(self, chat_id, event_title, minutes_to_event):
        message = f'Через {minutes_to_event} минут будет {event_title}!'
        token = os.getenv('TG_TOKEN')
        self.stdout.write(str(token))
        self.stdout.write(str(chat_id))
        self.stdout.write(str(message))
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
        response = requests.get(url)
        self.stdout.write(str(response))
