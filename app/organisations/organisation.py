from app.database import (
    Organisation as OrganisationModel,
    OrganisationsUsers as OrganisationsUsersModel,
)
from app.database.interface import DatabaseInterfaceWrapper
from app.organisations.organisation_schema import (
    OrganisationCreate as OrganisationCreate,
    Organisation as OrganisationSchema,
    OrganisationUpdate,
)
from app.users import User
from app.utils import (
    send_invite_email
)


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
    def init_class_instance(cls, schema_model):
        return cls(org=schema_model)

    def __init__(self, org: OrganisationSchema):
        self.organisation = org

    @property
    def fields(self) -> OrganisationSchema:
        return self.organisation

    def add_user(self, user: User) -> bool:
        org_user_model = OrganisationsUsersModel(
            organisation_id=self.fields.id,
            user_id=user.fields.id,
        )
        db_model = self.commit_to_db(model=org_user_model)

        if not db_model.id:
            return False
        return True

    def remove_user(self, user: User) -> bool:
        raise NotImplemented

    def invite_new_user(self, user: User) -> bool:
        if self.add_user(user=user):
            send_invite_email(
                user_name=user.fields.first_name,
                user_email=user.fields.email
            )
        else:
            return False
        return True

    def set_logo(self, image_bytes):
        pass

    def create_event(self, event_data: dict):
        # Create event
        # event = Event.create(data=event_data)

        # Find/create ScheduleTrigger and action
        # Todo

        # Create tracking event if necessary
        # Todo

        # Find/create ScheduleTrigger and action
        # Todo
        pass