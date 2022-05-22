import pytz
from celery_service import celery_app
from logger import logger
from celery.schedules import crontab
from app.workflows.triggers.trigger import ScheduledTrigger
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.workflows.actions.action import Action
from app.utils import timezoned_time


@celery_app.task
def run_periodic_scheduler():
    logger.info("Executing 'run_periodic_scheduler'")
    now = timezoned_time()
    filter_date = now + relativedelta(minutes=5)

    criteria = {
        'execute_date': {
            'operator': '<',
            'value': filter_date.strftime('%Y-%m-%d %H:%M:%S'),
        },
    }

    triggers = ScheduledTrigger.get_all_by(criteria=criteria)
    triggers_within_frame = [trigger for trigger in triggers if trigger.execute_date > now]

    for trigger in triggers_within_frame:
        actions = Action.get_all_by(criteria={
            'schedule_trigger_id': trigger.id,
        })

        for action in actions:
            Action(action=action).run()

    for trigger in triggers:
        ScheduledTrigger.delete(trigger.id)


@celery_app.task
def sync_database_with_messaging_platform():
    logger.info("Executing 'sync_database_with_messaging_platform'")


celery_app.conf.beat_schedule = {
    'scheduler': {
        'task': 'app.periodic_tasks.run_periodic_scheduler',
        'schedule': crontab(minute=1),
    }
}

# celery_app.conf.beat_schedule = {
#     'daily-sync': {
#         'task': 'app.periodic_tasks.sync_database_with_messaging_platform',
#         'schedule': crontab(hour=2),
#     }
# }
