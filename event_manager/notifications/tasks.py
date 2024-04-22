from celery import shared_task
from django.core.management import call_command


@shared_task()
def send_email_task():
    call_command('email_report')