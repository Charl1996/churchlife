from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    last_name: Optional[str] = None
    email: Optional[str] = None
    organisations: Optional[List[object]] = []


class User(UserBase):
    id: int
    organisations: List[object]

    class Config:
        orm_mode = True


class UserOrganisationView(BaseModel):
    domain: str
    name: str
    # logo: any

    class Config:
        orm_mode = True