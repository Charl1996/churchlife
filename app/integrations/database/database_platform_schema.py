from pydantic import BaseModel
from app.integrations.platform_schema import PlatformSchema
from typing import List, Optional


class BreezePlatformSchema(PlatformSchema):
    subdomain: str

    class Config:
        orm_mode = True


class Entity(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: Optional[str]
    age: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    tags: Optional[List[str]]
