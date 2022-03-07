from typing import List
from pydantic import BaseModel

from app.models.schemas import organisation


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    organisation_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    organisations: List[organisation.Organisation]

    class Config:
        orm_mode = True
