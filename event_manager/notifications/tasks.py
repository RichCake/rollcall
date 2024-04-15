from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_email_task(email_address, message):
    send_mail(
        'Уведомление!',
        f'\t{message}\n\nThank you!',
        'support@rollcall.com',
        [email_address],
        fail_silently=False,
    )