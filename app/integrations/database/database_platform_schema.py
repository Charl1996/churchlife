from pydantic import BaseModel
from app.integrations.platform_schema import PlatformSchema


class BreezePlatformSchema(PlatformSchema):
    subdomain: str

    class Config:
        orm_mode = True
