import pytz
from celery import Celery
from configs import RABBITMQ_URL


celery_app = Celery(
    'tasks',
    broker=RABBITMQ_URL,
    include=[
        'app.periodic_tasks',
    ]
)

# Configure Celery timezone to South African time
celery_app.conf.timezone = pytz.country_timezones['za'][0]
