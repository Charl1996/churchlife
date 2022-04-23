from app.database.interface import DatabaseInterfaceWrapper
from app.events import (
    Event as EventSchema,
    EventCreate,
)
from app.database.models import Event as EventModel


class Event(DatabaseInterfaceWrapper):

    event: EventSchema

    @classmethod
    def database_model(cls):
        return EventModel

    @classmethod
    def create_schema_model(cls):
        return EventCreate

    @classmethod
    def schema_model(cls):
        return EventSchema

    @classmethod
    def create_model(cls, create_schema: EventCreate):
        return EventModel(
            **create_schema
        )

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(event=schema_model)

    @classmethod
    def create_session(cls, model_id: int):
        event = cls.get(model_id=model_id)
        event.start_new_session()

    def __init__(self, event: EventSchema):
        self.event = event

    @property
    def fields(self) -> EventSchema:
        return self.event

    def start_new_session(self):
        pass

    def add_attendance_tracker(self, data: dict):
        # Find/create ScheduleTrigger and action
        # Todo
        pass
