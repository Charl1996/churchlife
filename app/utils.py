import pytz
from datetime import (
    datetime,
    timedelta,
)
from app.workflows.triggers.trigger import ScheduledTrigger

TIMEZONE = 'Africa/Johannesburg'
TIME_STRING_FORMAT = "%H:%M"


def send_invite_email(user_name: str, user_email: str):
    print(f'send_invite_email to {user_email}')
    return True


def offset_minutes(time_string: str, minutes: int):
    try:
        base_time = datetime.strptime(time_string, TIME_STRING_FORMAT)
    except ValueError:
        # This happens when there's an additional :00 appended to the end
        base_time = datetime.strptime(time_string[:5], TIME_STRING_FORMAT)

    offset_timestamp = base_time + timedelta(minutes=minutes)
    return "{hour}:{minute}:{second}".format(
        hour=offset_timestamp.hour,
        minute=offset_timestamp.minute,
        second=offset_timestamp.second,
    )


def create_scheduler_actions(execute_date: any, action_type: str, action_data: dict):
    trigger = ScheduledTrigger.find_or_create_by_execution_date(
        date=execute_date.strftime('%Y-%m-%d %H:%M:%S'),
    )

    trigger.create_action(
        action_type=action_type,
        action_data=action_data,
    )


def timezoned_time():
    now = datetime.now(tz=pytz.timezone(TIMEZONE))
    return datetime.strptime(now.strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
