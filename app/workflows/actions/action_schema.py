from typing import Any, Optional
from pydantic import BaseModel


class ActionData(BaseModel):
    method: str
    args: Any


class ActionCreate(BaseModel):
    type: str
    data: ActionData
    tracking_event_trigger_id: Optional[str]
    schedule_trigger_id: Optional[str]


class Action(ActionCreate):
    id: str

    class Config:
        orm_mode = True
