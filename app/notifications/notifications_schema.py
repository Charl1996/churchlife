from pydantic import BaseModel


class NotificationCreate(BaseModel):
    name: str
    organisation_id: str


class Notification(NotificationCreate):
    id: str

    class Config:
        orm_mode = True


class NotificationItem(BaseModel):
    notification_id: str
    type: str
    data: dict

    class Config:
        orm_mode = True
