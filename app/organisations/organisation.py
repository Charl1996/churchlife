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
# from app.events.event_schema import EventCreate
from app.utils import (
    send_invite_email
)
from app.integrations.database.database_platform import PlatformModel, PlatformSchema, DATABASE_PLATFORM_TYPE
from app.integrations.database.breeze_platform import BreezeDatabasePlatform, BreezePlatformSchema
from app.integrations.messaging.messaging_platform import MESSAGING_PLATFORM_TYPE
from app.integrations.messaging.respondio_platform import RespondIOMessagingPlatform
from app.notifications import Notification, NotificationSchema
from typing import List

ACTIVE_STATUS = 'active'
PENDING_STATUS = 'pending'


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

    def create_event(self, detail: dict, attendance=None):
        breakpoint()
        detail['organisation_id'] = self.fields.id

        # Todo:
        # CREATE IN TRANSACTION

        # Create event
        # event = Event.create(data=event_data)

        # Find/create ScheduleTrigger and action for event

        # Determine attendance tracking event

        # Find/create ScheduleTrigger and action for attendance event

        # Create notification

        # Link notification to event

        pass

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
