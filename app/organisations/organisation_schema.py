from typing import Optional, List
from pydantic import BaseModel


class OrganisationBase(BaseModel):
    domain: str
    name: str


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationUpdate(BaseModel):
    name: Optional[str] = None
    users: Optional[List[object]] = []


class Organisation(OrganisationBase):
    id: int
    users: List[object]

    class Config:
        orm_mode = True


# class OrganisationView(OrganisationBase):
#     logo: any
#     events: List[object]
#
#     class Config:
#         orm_mode = True