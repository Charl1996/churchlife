from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.database import (
    Organisation as OrganisationModel,
    OrganisationsUsers as OrganisationsUsersModel,
)
from app.database.interface import DatabaseInterfaceWrapper
from app.organisations.organisation_schema import (
    OrganisationCreate as OrganisationCreate,
    Organisation as OrganisationSchema,
    OrganisationUpdate,
    OrganisationsUsersSchema,
    OrganisationUserViewSchema,
)
from app.utils import (
    send_invite_email
)
from app.integrations.database.database_platform import PlatformModel, PlatformSchema, DATABASE_PLATFORM_TYPE
from app.integrations.database.breeze_platform import BreezeDatabasePlatform, BreezePlatformSchema
from app.integrations.messaging.messaging_platform import MESSAGING_PLATFORM_TYPE
from app.integrations.messaging.respondio_platform import RespondIOMessagingPlatform
from app.notifications import Notification, NotificationSchema
from app.utils import create_scheduler_actions
from app.utils import offset_minutes
from typing import List
import pytz

ACTIVE_STATUS = 'active'
PENDING_STATUS = 'pending'
TIMEZONE = 'Africa/Johannesburg'


class Organisation(DatabaseInterfaceWrapper):

    organisation: OrganisationSchema

    @classmethod
    def database_model(cls):
        return OrganisationModel

    @classmethod
    def create_schema_model(cls):
        return OrganisationCreate

    @classmethod
    def schema_model(cls):
        return OrganisationSchema

    @classmethod
    def create_model(cls, create_schema: OrganisationCreate):
        return OrganisationModel(
            name=create_schema.name,
            domain=create_schema.domain,
        )

    @classmethod
    def get_by_domain(cls, domain: str):
        org_schema = super().get_by(field="domain", value=domain)
        return cls(org=org_schema)

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(org=schema_model)

    def __init__(self, org: OrganisationSchema):
        self.organisation = org

    @property
    def fields(self) -> OrganisationSchema:
        return self.organisation

    def add_user(self, user, status=ACTIVE_STATUS) -> bool:
        org_user_model = OrganisationsUsersModel(
            organisation_id=self.fields.id,
            user_id=user.fields.id,
            status=status,
        )
        db_model = self.commit_to_db(model=org_user_model)

        if not db_model.id:
            return False
        return True

    def get_user_status(self, user_id: str) -> str:
        criteria = {
            'organisation_id': self.fields.id,
            'user_id': user_id,
        }
        result = self.get_by(
            model=OrganisationsUsersModel,
            schema=OrganisationsUsersSchema,
            criteria=criteria,
        )
        return result.status

    def remove_user(self, user_id: str) -> bool:
        org_user = self.get_by(
            model=OrganisationsUsersModel,
            schema=OrganisationsUsersSchema,
            criteria={'user_id': user_id, 'organisation_id': self.fields.id},
        )
        if not org_user:
            return False

        self.delete(model=OrganisationsUsersModel, model_id=org_user.id)
        return True

    def invite_new_user(self, user) -> bool:
        if self.add_user(user=user, status=PENDING_STATUS):
            send_invite_email(
                user_name=user.fields.first_name,
                user_email=user.fields.email
            )
        else:
            return False
        return True

    def set_logo(self, image_bytes):
        pass

    def get_events(self):
        from app.events import Event
        return Event.get_all_by(criteria={'organisation_id': self.fields.id})

    def get_upcoming_events(self):
        from app.events.event_schema import EventListItem
        from app.events import Event
        events = self.get_events()

        session_events = []

        for event in events:
            session_event = Event.get_upcoming_event(event_id=event.id)
            if session_event:
                session_events.append(EventListItem(
                    id=session_event.fields.id,
                    name=event.name,
                    date=session_event.readable_date,
                    start_time=session_event.start_time,
                    end_time=session_event.end_time
                ))

        return session_events

    def get_past_events(self):
        from app.events.event_schema import EventListItem
        from app.events import Event
        events = self.get_events()

        session_events = []

        for event in events:
            session_event = Event.get_past_events(event_id=event.id)
            if session_event:
                session_events.append(EventListItem(
                    id=session_event.fields.id,
                    name=event.name,
                    date=session_event.readable_date,
                    start_time=session_event.start_time,
                    end_time=session_event.end_time
                ))

        return session_events

    def create_event(self, event_detail: dict, attendance_tracking_detail=dict):
        from app.events import Event, TrackingEvent

        event = Event.create(data=event_detail)

        tracker_triggers = attendance_tracking_detail.pop('triggers')
        attendance_tracking_detail['event_id'] = event.fields.id

        attendance_tracking_detail['start_time'] = offset_minutes(
            event_detail['start_time'],
            -1*int(attendance_tracking_detail['start_before']),
        )
        attendance_tracking_detail['end_time'] = offset_minutes(
            event_detail['end_time'],
            int(attendance_tracking_detail['stop_after']),
        )

        attendance_tracking_detail['from_date'] = event_detail['from_date']
        attendance_tracking_detail['to_date'] = event_detail['to_date']
        attendance_tracking_detail['type'] = event_detail['type']
        attendance_tracking_detail['interval'] = event_detail['interval']

        tracking_event = TrackingEvent.set_up_tracking_event(
            data=attendance_tracking_detail,
            triggers=tracker_triggers,
        )

        self._initialize_scheduled_sessions(
            start_time=event.fields.start_time,
            date=event.fields.from_date,
            interval=event.fields.interval,
            action_data={
                'method': 'execute_trigger_event',
                'args': [
                    'Event.create_event_session',
                    event.fields.id,
                    'from app.events.event import Event'
                ],
            },
        )

        # Create scheduled sessions for tracking event
        self._initialize_scheduled_sessions(
            start_time=tracking_event.fields.start_time,
            date=tracking_event.fields.from_date,
            interval=event.fields.interval,
            action_data={
                'method': 'execute_trigger_event',
                'args': [
                    'TrackingEvent.create_event_session',
                    tracking_event.fields.id,
                    'from app.events.event import TrackingEvent'
                ],
            },
        )

    def get_users(self) -> List[OrganisationUserViewSchema]:
        from app.users import User

        criteria = {'organisation_id': self.fields.id}
        result = self.get_all_by(
            model=OrganisationsUsersModel,
            schema=OrganisationsUsersSchema,
            criteria=criteria,
        )

        users_results = []
        for org_user in result:
            user = User.get_by_id(user_id=org_user.user_id)
            detailed_user = OrganisationUserViewSchema(
                id=user.fields.id,
                first_name=user.fields.first_name,
                last_name=user.fields.last_name,
                email=user.fields.email,
                status=org_user.status,
            )
            users_results.append(detailed_user)

        return users_results

    def get_linked_database_platform(self):
        criteria = {
            'type': DATABASE_PLATFORM_TYPE,
            'organisation_id': self.fields.id,
        }

        result = self.get_by(
            model=PlatformModel,
            schema=PlatformSchema,
            criteria=criteria,
        )

        if not result:
            return None

        # Better way to do this?
        if result.slug == BreezeDatabasePlatform.slug:
            result = self.get_by(
                model=PlatformModel,
                schema=BreezePlatformSchema,
                criteria=criteria,
            )

        return result

    def get_linked_messaging_platform(self):
        criteria = {
            'type': MESSAGING_PLATFORM_TYPE,
            'organisation_id': self.fields.id,
        }

        result = self.get_by(
            model=PlatformModel,
            schema=PlatformSchema,
            criteria=criteria,
        )

        if not result:
            return None

        # Better way to do this?
        if result.slug == RespondIOMessagingPlatform.slug:
            result = self.get_by(
                model=PlatformModel,
                schema=PlatformSchema,
                criteria=criteria,
            )

        return result

    def update_details(self, data: dict):
        organisation_details = OrganisationUpdate(**data)
        self.update_by_id(model_id=self.fields.id, model_changes=organisation_details)

    @property
    def updateable_details(self):
        return OrganisationUpdate(**self.fields.dict())

    def get_notifications(self) -> List[NotificationSchema]:
        return Notification.get_all_by(
            criteria={
                'organisation_id': self.fields.id
            }
        )

    def _initialize_scheduled_sessions(self, start_time, date, interval, action_data):
        from app.workflows.actions.action import Action

        delta_time = relativedelta(hours=start_time.hour, minutes=start_time.minute)
        execution_date = date + delta_time
        now = datetime.now(tz=pytz.timezone(TIMEZONE))

        if not interval:
            # Create events without interval one week before
            interval = 'weekly'

        interval_delta = None

        if interval == 'daily':
            interval_delta = relativedelta(days=1)
        elif interval == 'weekly':
            interval_delta = relativedelta(weeks=1)
        elif interval == 'monthly':
            interval_delta = relativedelta(months=1)

        if interval_delta:
            execution_date_minus_one_interval_date = execution_date - interval_delta

            if execution_date_minus_one_interval_date.date() > now.date():
                execution_date = execution_date_minus_one_interval_date
            else:
                execution_date = now

        execution_date = execution_date.date() + relativedelta(
            hours=execution_date.hour,
            minutes=execution_date.minute
        )

        create_scheduler_actions(
            execute_date=execution_date,
            action_type=Action.FUNCTION,
            action_data=action_data
        )
