from sqlalchemy.orm import Session

from app.database import (
    Organisation as OrganisationModel,
    OrganisationsUsers as OrganisationsUsersModel,
)
from app.database.operations import CRUDOperations
from app.organisations.organisation_schema import (
    OrganisationCreate as OrganisationCreate,
    Organisation,
    OrganisationUpdate,
)
from app.users.user_schema import User
from app.utils import (
    send_invite_email
)


class OrganisationHandler(CRUDOperations):

    @classmethod
    def get_database_model(cls):
        return OrganisationModel

    @classmethod
    def get_schema_model(cls):
        return Organisation

    @classmethod
    def create(cls, db: Session, organisation: OrganisationCreate):
        org_model = OrganisationModel(
            name=organisation.name,
            domain=organisation.domain,
        )
        org_model = cls.commit_to_db(db=db, model=org_model)
        return cls.get_schema_model().from_orm(org_model)

    @classmethod
    def add_user_to_organisation(cls, db: Session, user: User, organisation: Organisation):
        org_user_model = OrganisationsUsersModel(
            organisation_id=organisation.id,
            user_id=user.id,
        )

        cls.commit_to_db(db=db, model=org_user_model)

    @classmethod
    def invite_new_user_to_organisation(cls, db: Session, user: User, organisation: Organisation):
        cls.add_user_to_organisation(db=db, user=user, organisation=organisation)
        send_invite_email(user.first_name, user.email)
