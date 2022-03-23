from sqlalchemy.orm import Session

from app.database import (
    Organisation as OrganisationModel,
    OrganisationsUsers as OrganisationsUsersModel,
)
from app.database.interface import DatabaseInterface
from app.organisations.organisation_schema import (
    OrganisationCreate as OrganisationCreate,
    Organisation as OrganisationSchema,
    OrganisationUpdate,
)
from app.users import User
from app.utils import (
    send_invite_email
)


class Organisation(DatabaseInterface):

    organisation: OrganisationSchema

    @classmethod
    def database_model(cls):
        return OrganisationModel

    @classmethod
    def schema_model(cls):
        return OrganisationSchema

    @classmethod
    def create(cls, data: dict):
        organisation_create = OrganisationCreate(**data)

        org_model = OrganisationModel(
            name=organisation_create.name,
            domain=organisation_create.domain,
        )
        org_schema = super().create(model_data=org_model)
        return cls(org=org_schema)

    @classmethod
    def get(cls, org_id: int):
        org_schema = super().get(model_id=org_id)
        if not org_schema:
            return None
        return cls(org=org_schema)

    @classmethod
    def delete(cls, org_id: int):
        # Do user specific stuff here
        # - Remove OrganisationUser
        super().delete(model_id=org_id)

    @classmethod
    def get_by_domain(cls, domain: str):
        org_schema = super().get_by(field="domain", value=domain)
        if not org_schema:
            return None
        return cls(org=org_schema)

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
