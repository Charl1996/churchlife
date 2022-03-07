from sqlalchemy.orm import Session
from app.models import Organisation
from app.models.crud.decorators import insert
from app.models.schemas.organisation import OrganisationCreate


@insert
def create_organisation(organisation: OrganisationCreate):
    return Organisation(
        name=organisation.name,
        domain=organisation.domain,
    )


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
