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

class OrganisationsUsersSchema(BaseModel):
    id: str
    organisation_id: str
    user_id: str
    status: str

    class Config:
        orm_mode = True


class OrganisationUserViewSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    status: Optional[str]
