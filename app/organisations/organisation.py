from sqlalchemy.orm import Session
from app.database.operations import (
    insert
)
from app.database import Organisation as DBOrganisation
from app.organisations.organisation_schema import OrganisationCreate, Organisation


def create_organisation(db: Session, organisation: OrganisationCreate) -> Organisation:
    data_model = DBOrganisation(
        name=organisation.name,
        domain=organisation.domain,
    )
    result = insert(db, data_model)
    # Send back schema organisation?
    return result


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
