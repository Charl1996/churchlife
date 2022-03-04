import pytz

from celery import Celery
from configs import BROKER_URL


celery_app = Celery(
    'tasks',
    broker=BROKER_URL,
    include=[
        'app.periodic_tasks',
        'app.messaging.tasks',
    ]
)

# Configure Celery timezone to South African time
celery_app.conf.timezone = pytz.country_timezones['za'][0]
