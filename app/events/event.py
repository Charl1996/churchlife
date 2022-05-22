import datetime
from dateutil.relativedelta import relativedelta
import pytz
from app.database.interface import DatabaseInterfaceWrapper
from app.events.event_schema import (
    Event as EventSchema,
    EventCreate as EventCreateSchema,
    TrackingEvent as TrackingEventSchema,
    TrackingEventCreate as TrackingEventCreateSchema,
    SessionEventCreate as SessionEventCreateSchema,
    SessionEvent as SessionEventSchema,
    SessionEventDetails as SessionEventDetailsSchema,
)
from app.database.models import (
    Event as EventModel,
    TrackingEvent as TrackingEventModel,
    EventSession as EventSessionModel,
    TrackingEventSession as TrackingEventSessionModel,
)
from app.workflows.triggers.trigger import TrackingEventTrigger
from app.workflows.actions.action import Action

TIMEZONE = 'Africa/Johannesburg'


class BaseEvent(DatabaseInterfaceWrapper):

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(event=schema_model)

    @classmethod
    def create_event_session(cls, model_id: int, calculate_session_date=False):
        event = cls.get(model_id=model_id)
        event.create_new_session(calculate_session_date=calculate_session_date)
        # Todo
        # Create schedule trigger to start session

    @classmethod
    def start_event_session(cls, event_id, ):
        # Todo
        # Create schedule trigger to stop session
        pass

    @classmethod
    def stop_event_session(cls):
        # Todo
        # Create schedule trigger to create session event if not end date reached
        pass

    @classmethod
    def session_class(cls):
        raise NotImplemented

    def create_new_session(self, calculate_session_date=False):
        if calculate_session_date:
            # self.fields.from_date.weekday()
            session_date = self._get_closets_date_after_today_with_interval(
                interval=self.fields.interval,
            )
        else:
            session_date = datetime.datetime.now(tz=pytz.timezone(TIMEZONE)) + self.interval_delta()

        if type(self.fields) == EventSchema:
            event_type_id = 'event_id'
        if type(self.fields) == TrackingEventSchema:
            event_type_id = 'tracking_event_id'

        SessionEvent.create(data={
            'active': False,
            'start_time': self.fields.start_time.strftime('%H:%M'),
            'end_time': self.fields.end_time.strftime('%H:%M'),
            'date': session_date.strftime('%Y-%m-%d %H:%M:%S'),
            event_type_id: self.fields.id,
        })

    def interval_delta(self):
        interval = self.fields.interval

        if not interval:
            interval = 'weekly'

        if interval == 'daily':
            return relativedelta(days=1)
        elif interval == 'weekly':
            return relativedelta(weeks=1)
        elif interval == 'monthly':
            return relativedelta(months=1)
        return relativedelta(days=0)

    def _get_closets_date_after_today_with_interval(self, interval='weekly') -> datetime.datetime:
        now = datetime.datetime.now(tz=pytz.timezone(TIMEZONE))
        if interval == 'daily':
            start_time = self.fields.start_time
            if now.hour < start_time.hour:
                return now
            else:
                return now + relativedelta(days=1)
        elif interval == 'weekly':
            weekday_diff = self.fields.from_date.weekday() - now.weekday()

            if weekday_diff < 0:
                # Event already occurred in this week
                return now + relativedelta(weeks=1, days=-weekday_diff)
            elif weekday_diff > 0:
                # Event must still occur in this week
                return now + relativedelta(days=weekday_diff)
            else:
                return now
        elif interval == 'monthly':
            month_diff = self.fields.from_date.month - now.month

            if month_diff < 0:
                return self.fields.from_date + relativedelta(months=1)
            elif month_diff > 0:
                return self.fields.from_date
            else:
                return self.fields.from_date


class Event(BaseEvent):

    event: EventSchema

    @classmethod
    def database_model(cls):
        return EventModel

    @classmethod
    def create_schema_model(cls):
        return EventCreateSchema

    @classmethod
    def schema_model(cls):
        return EventSchema

    @classmethod
    def create_model(cls, create_schema: EventCreateSchema):
        return EventModel(
            name=create_schema.name,
            from_date=create_schema.from_date,
            to_date=create_schema.to_date or None,
            start_time=create_schema.start_time,
            end_time=create_schema.end_time,
            interval=create_schema.interval,
            type=create_schema.type,
            organisation_id=create_schema.organisation_id,
            event_data=create_schema.event_data,
        )

    @classmethod
    def session_class(cls):
        return EventSessionModel

    def __init__(self, event: EventSchema):
        self.event = event

    @property
    def fields(self) -> EventSchema:
        return self.event

    @classmethod
    def get_upcoming_event(cls, event_id):

        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H:%M')

        sessions = SessionEvent.get_all_by(criteria={
            'event_id': event_id,
        })

        now = format_datetime(datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))
        # Could be improved
        sessions = [SessionEvent(session_event=session) for session in sessions if format_datetime(session.date) > now]

        if sessions:
            return sessions[0]
        return None

    @classmethod
    def get_past_events(cls, event_id):
        def format_datetime(dt):
            return dt.strftime('%Y-%m-%d %H:%M')

        now = format_datetime(datetime.datetime.now(tz=pytz.timezone(TIMEZONE)))

        def is_past_event(session):
            end_time = datetime.datetime.strptime(session.end_time, '%H:%M')
            relative_time = relativedelta(hours=end_time.hour, minutes=end_time.minute)

            session_date = datetime.datetime.strptime(session.date.strftime('%Y-%m-%d'), '%Y-%m-%d')
            session_time_delta = session_date + relative_time
            return session_time_delta < datetime.datetime.strptime(now, '%Y-%m-%d %H:%M')

        sessions = SessionEvent.get_all_by(criteria={
            'event_id': event_id,
        })

        # Could be improved
        sessions = [SessionEvent(session_event=session) for session in sessions if is_past_event(session)]

        if sessions:
            return sessions[0]
        return None

    def get_session_by_id(self, event_session_id):
        session_event = SessionEvent.get(event_session_id)
        return SessionEvent(session_event=session_event)


class TrackingEvent(BaseEvent):
    event: TrackingEventSchema

    @classmethod
    def database_model(cls):
        return TrackingEventModel

    @classmethod
    def create_schema_model(cls):
        return TrackingEventCreateSchema

    @classmethod
    def schema_model(cls):
        return TrackingEventSchema

    @classmethod
    def create_model(cls, create_schema: TrackingEventCreateSchema):
        return TrackingEventModel(
            from_date=create_schema.from_date,
            to_date=create_schema.to_date or None,
            start_time=create_schema.start_time,
            end_time=create_schema.end_time,
            interval=create_schema.interval,
            event_id=create_schema.event_id,
            type=create_schema.type,
        )

    @classmethod
    def set_up_tracking_event(cls, data: dict, triggers: dict):
        tracking_event = cls.create(data=data)

        for trigger in triggers:
            trigger_type = trigger.pop('type')
            trigger_obj = TrackingEventTrigger.create(data={
                'type': trigger_type,
                'tracking_event_id': tracking_event.fields.id,
            })

            action_args = [
                trigger['notification_id'],
                tracking_event.fields.id,
                trigger_type,
            ]
            trigger_obj.create_action(
                action_type=Action.FUNCTION,
                action_data={
                    'method': 'send_trigger_notification',
                    'args': action_args,
                }
            )
        return tracking_event

    @classmethod
    def session_class(cls):
        return TrackingEventSessionModel

    def __init__(self, event: TrackingEventSchema):
        self.event = event

    @property
    def fields(self) -> TrackingEventSchema:
        return self.event

    def new_face_detected(self):
        pass

    def familiar_face_detected(self):
        pass

    def finish(self):
        pass


class SessionEvent(DatabaseInterfaceWrapper):
    session_event: SessionEventSchema

    @classmethod
    def database_model(cls):
        return EventSessionModel

    @classmethod
    def create_schema_model(cls):
        return SessionEventCreateSchema

    @classmethod
    def schema_model(cls):
        return SessionEventSchema

    @classmethod
    def create_model(cls, create_schema: SessionEventCreateSchema):
        # Why create_schema.date offset with 2h?
        return cls.database_model()(
            active=create_schema.active,
            event_id=create_schema.event_id or None,
            tracking_event_id=create_schema.tracking_event_id or None,
            start_time=create_schema.start_time,
            end_time=create_schema.end_time,
            date=create_schema.date.strftime('%Y-%m-%d %H:%M:%S'),
            event_data=create_schema.event_data,
        )

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(session_event=schema_model)

    def __init__(self, session_event: SessionEventSchema):
        self.session_event = session_event

    @property
    def readable_date(self):
        return self.fields.date.strftime('%d %b %Y')

    @property
    def start_time(self):
        return self.fields.start_time

    @property
    def end_time(self):
        return self.fields.end_time

    @property
    def fields(self) -> SessionEventSchema:
        return self.session_event

    def stats(self):
        """
        e.g.
        {
            <custom_key>: <custom_value>,
        }
        """
        return self.fields.event_data

    def event_details(self) -> SessionEventDetailsSchema:
        event = Event.get(self.fields.event_id)
        event_data = self.fields.dict()
        event_data['name'] = event.fields.name
        return SessionEventDetailsSchema(**event_data)
