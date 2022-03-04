from celery_service import celery_app
from logger import logger
from celery.schedules import crontab


@celery_app.task
def sync_database_with_messaging_platform():
    logger.info("sync_database_with_messaging_platform is executing!")


celery_app.conf.beat_schedule = {
    'daily-sync': {
        'task': 'app.periodic_tasks.sync_database_with_messaging_platform',
        'schedule': crontab(hour=2),
    }
}
