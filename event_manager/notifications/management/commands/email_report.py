import datetime as dt

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from events.models import Event


class Command(BaseCommand):
    help = """Sends notifications to participants
     of an event that's coming up in an hour"""

    def handle(self, *args, **options):
        coming_events = Event.objects.get_public_events().filter(
            end__gte=timezone.now(),
            end__lte=timezone.now() + dt.timedelta(hours=1),
            )
        for event in coming_events:
            minutes_to_event = (event.end - timezone.now()).seconds // 60
            participants = event.eventparticipants_set.filter(notified=False)
            for participant in participants:
                send_mail(
                    'Уведомление!',
                    f'\t{participant.user.username},\n'
                    f'\tЧерез {minutes_to_event} минут будет {event.title}!'
                    '\n\nПисьмо отправлено автоматически, '
                    'не отвечайте на него.',
                    'noreply@rollcall.com',
                    [participant.user.email],
                    fail_silently=False,
                )
                participant.notified = True
                participant.save()
        self.stdout.write('E-mail Report was sent.')
