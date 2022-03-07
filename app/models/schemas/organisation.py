from typing import List
from pydantic import BaseModel

from app.models.schemas import user


class OrganisationBase(BaseModel):
    domain: str
    name: str


class OrganisationCreate(OrganisationBase):
    pass


class Organisation(OrganisationBase):
    id: int
    users: List[user.User]

    class Config:
        orm_mode = True
