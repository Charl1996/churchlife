from typing import Optional, Any
from pydantic import BaseModel
import datetime

Datetime = datetime.datetime
Time = datetime.time


class EventBase(BaseModel):
    name: str
    type: str
    interval: str
    organisation_id: int


class EventCreate(EventBase):
    from_date: str
    to_date: Optional[str]
    start_time: str
    end_time: Optional[str]
    event_data: Optional[Any]


class EventUpdate(EventBase):
    from_date: Datetime
    to_date: Optional[Datetime]
    start_time: Time
    end_time: Time
    event_data: Optional[Any]


class Event(EventBase):
    id: int
    from_date: Datetime
    to_date: Optional[Datetime]
    start_time: Time
    end_time: Time
    name: str
    type: str
    interval: str

    class Config:
        orm_mode = True


class TrackingEventBase(BaseModel):
    interval: str
    type: str
    event_id: str


class TrackingEventCreate(TrackingEventBase):
    from_date: str
    to_date: Optional[str]
    start_time: str
    end_time: str


class TrackingEvent(TrackingEventBase):
    id: int
    from_date: Datetime
    to_date: Optional[Datetime]
    start_time: Time
    end_time: Time

    class Config:
        orm_mode = True


class SessionEventCreate(BaseModel):
    active: bool
    start_time: str
    end_time: str
    date: Datetime
    event_data: Optional[Any]
    event_id: Optional[str]
    tracking_event_id: Optional[str]


class SessionEvent(SessionEventCreate):
    id: str

    class Config:
        orm_mode = True


class EventListItem(BaseModel):
    id: int
    name: str
    date: str  # eg. 5 March 2022
    start_time: str
    end_time: str


class SessionEventDetails(BaseModel):
    start_time: Time
    end_time: Time
    name: str
    active: bool
    date: Datetime
    event_data: Optional[Any]
