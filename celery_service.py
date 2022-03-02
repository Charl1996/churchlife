from celery import Celery
from configs import BROKER_URL


celery_app = Celery(
    'tasks',
    broker=BROKER_URL,
    include=[
        'app.messaging.tasks',
    ]
)
