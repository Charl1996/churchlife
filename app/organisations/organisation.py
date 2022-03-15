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

    # Make sure all these db_session's are closed after each request
    db_session: Session
    organisation: OrganisationSchema

    @classmethod
    def database_model(cls):
        return OrganisationModel

    @classmethod
    def schema_model(cls):
        return OrganisationSchema

    @classmethod
    def create(cls, db_session: Session, data: dict):
        organisation_create = OrganisationCreate(**data)

        org_model = OrganisationModel(
            name=organisation_create.name,
            domain=organisation_create.domain,
        )
        org_schema = super().create(db_session=db_session, model_data=org_model)
        return cls(db_session=db_session, org=org_schema)

    @classmethod
    def get(cls, db_session: Session, org_id: int):
        org_schema = super().get(db_session=db_session, model_id=org_id)
        if not org_schema:
            return None
        return cls(db_session=db_session, org=org_schema)

    @classmethod
    def delete(cls, db_session: Session, org_id: int):
        # Do user specific stuff here
        # - Remove OrganisationUser
        super().delete(db_session=db_session, model_id=org_id)

    @classmethod
    def get_by_domain(cls, db_session: Session, domain: str):
        org_schema = super().get_by(db_session=db_session, field="domain", value=domain)
        if not org_schema:
            return None
        return cls(db_session=db_session, org=org_schema)

    def __init__(self, db_session: Session, org: OrganisationSchema):
        self.db_session = db_session
        self.organisation = org

    @property
    def fields(self) -> OrganisationSchema:
        return self.organisation

    def add_user(self, user: User) -> bool:
        org_user_model = OrganisationsUsersModel(
            organisation_id=self.fields.id,
            user_id=user.fields.id,
        )
        db_model = self.commit_to_db(db_session=self.db_session, model=org_user_model)

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
