from typing import Any
from pydantic import BaseModel


class ScheduleTriggerCreate(BaseModel):
    execute_date: Any


class ScheduleTrigger(ScheduleTriggerCreate):
    id: str

    class Config:
        orm_mode = True


class TrackingEventTriggerCreate(BaseModel):
    type: str
    tracking_event_id: str


class TrackingEventTrigger(TrackingEventTriggerCreate):
    id: str

    class Config:
        orm_mode = True
