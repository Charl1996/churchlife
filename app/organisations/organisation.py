from sqlalchemy.orm import Session
from app.database.operations import (
    insert,
    update,
)
from app.database import Organisation as DBOrganisation
from app.organisations.organisation_schema import OrganisationCreate, Organisation
from app.utils import (
    send_invite_email
)


def create_organisation(db: Session, organisation: OrganisationCreate) -> Organisation:
    data_model = DBOrganisation(
        name=organisation.name,
        domain=organisation.domain,
    )
    result = insert(db, data_model)
    # Send back schema organisation?
    return result


def invite_user_to_organisation(db, user, organisation):
    add_user_to_organisation(user=user, organisation=organisation, db=db)
    send_invite_email(user.first_name, user.email)


def add_user_to_organisation(user, organisation, db):
    organisation.users.append(user)
    update(db=db)

# def get_organisation_by_id(db: Session, org_id: int):
#     pass
#
#
# def get_organisation_by_domain(db: Session, domain: str):
#     pass
#
#
# def get_all_organisations(db: Session):
#     pass
