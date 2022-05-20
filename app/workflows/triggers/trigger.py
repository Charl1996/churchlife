from collections import namedtuple
from app.database.interface import DatabaseInterfaceWrapper
from app.workflows.triggers import (
    ScheduleTriggerCreateSchema,
    ScheduleTriggerSchema,
    TrackingEventTriggerCreateSchema,
    TrackingEventTriggerSchema,
)
from app.database.models import (
    ScheduleTrigger as ScheduleTriggerModel,
    TrackingEventTrigger as TrackingEventTriggerModel,
)


SCHEDULE = 'schedule'
TRACKING_EVENT = 'tracking_event'


class Trigger(DatabaseInterfaceWrapper):

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(trigger=schema_model)

    def create_action(self, action_type: str, action_data: dict):
        from app.workflows.actions.action import Action
        action_trigger_type_key = ''

        if self.type == ScheduledTrigger.type:
            action_trigger_type_key = 'schedule_trigger_id'
        if self.type == TrackingEventTrigger.type:
            action_trigger_type_key = 'tracking_event_trigger_id'

        if action_trigger_type_key:
            Action.create(data={
                action_trigger_type_key: self.fields.id,
                'type': action_type,
                'data': action_data,
            })
        else:
            raise Exception(f'Action type not supported: {self.type}')


class ScheduledTrigger(Trigger):
    type = SCHEDULE

    @classmethod
    def database_model(cls):
        return ScheduleTriggerModel

    @classmethod
    def create_schema_model(cls):
        return ScheduleTriggerCreateSchema

    @classmethod
    def schema_model(cls):
        return ScheduleTriggerSchema

    @classmethod
    def create_model(cls, create_schema: ScheduleTriggerCreateSchema):
        return cls.database_model()(
            execute_date=create_schema.execute_date,
        )

    @classmethod
    def find_or_create_by_execution_date(cls, date: str):
        trigger = ScheduledTrigger.get_by(criteria={'execute_date': date})

        if trigger:
            return cls(trigger=trigger)

        return cls.create(data={'execute_date': date})

    def __init__(self, trigger: ScheduleTriggerSchema):
        self.trigger = trigger

    @property
    def fields(self) -> ScheduleTriggerSchema:
        return self.trigger

    @property
    def trigger_type(self):
        return self.type


TriggerType = namedtuple('TriggerType', ('type', 'display_item_text'))


class TrackingEventTrigger(Trigger):
    ON_DONE = TriggerType(type='on_done', display_item_text='done')

    SUPPORTED_TYPES = [
        ON_DONE,
    ]

    type = TRACKING_EVENT

    @classmethod
    def database_model(cls):
        return TrackingEventTriggerModel

    @classmethod
    def create_schema_model(cls):
        return TrackingEventTriggerCreateSchema

    @classmethod
    def schema_model(cls):
        return TrackingEventTriggerSchema

    @classmethod
    def create_model(cls, create_schema: TrackingEventTriggerCreateSchema):
        return cls.database_model()(
            type=create_schema.type,
            tracking_event_id=create_schema.tracking_event_id
        )

    def __init__(self, trigger: TrackingEventTriggerSchema):
        self.trigger = trigger

    @property
    def fields(self) -> TrackingEventTriggerSchema:
        return self.trigger

    @property
    def trigger_type(self):
        return self.type
