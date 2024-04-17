import datetime as dt

from django.core.mail import send_mail
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import periodic_task

from events.models import Event


@periodic_task(crontab(minute='*/1'))
def check_notifications_to_send():
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
                '\n\nПисьмо отправлено автоматически, не отвечайте на него.',
                'notifications@rollcall.com',
                [participant.user.email],
                fail_silently=False,
            )
            participant.notified = True
            participant.save()
