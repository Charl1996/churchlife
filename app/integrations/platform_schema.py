from pydantic import BaseModel


class PlatformSchema(BaseModel):
    slug: str
    api_key: str
    organisation_id: str
    type: str

    class Config:
        orm_mode = True