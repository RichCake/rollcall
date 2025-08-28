import os
import time

import requests
from celery import Celery
from django.utils import timezone
from django.conf import settings
from celery.utils.log import get_task_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_manager.settings')
app = Celery('event_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.task(bind=True)
def long_task(self):
    time.sleep(60)
    return 1


@app.task(bind=True)
def send_notification(self, minutes_to_event, event_title, chat_id):
    message = f'Через {minutes_to_event} минут будет {event_title}!'
    url = f'https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={chat_id}&text={message}'
    logger.info(url)
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data
    except requests.exceptions.Timeout as e:
        logger.error("Timeout error while sending notification", e)
        return e
    except requests.exceptions.JSONDecodeError as e:
        logger.error("Error while decoding response from api.telegram.org", e)
        return e
