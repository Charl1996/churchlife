from typing import Optional, List
from datetime import datetime
from time import time
from pydantic import BaseModel


class EventBase(BaseModel):
    from_date: datetime
    to_date: Optional[datetime]
    start_time: time
    end_time: Optional[time]
    interval: str
    organisation_id: int


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    from_date: datetime
    to_date: datetime
    start_time: time
    end_time: time


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
