from app.database.interface import DatabaseInterfaceWrapper
from app.workflows.triggers.trigger import TrackingEventTrigger
from app.database.models import Action as ActionModel
from app.workflows.actions import ActionSchema, ActionCreateSchema, ActionDataSchema


class Action(DatabaseInterfaceWrapper):
    # Action types
    FUNCTION = 'function'

    @classmethod
    def database_model(cls):
        return ActionModel

    @classmethod
    def create_schema_model(cls):
        return ActionCreateSchema

    @classmethod
    def schema_model(cls):
        return ActionSchema

    @classmethod
    def create_model(cls, create_schema: ActionCreateSchema):
        return cls.database_model()(
            type=create_schema.type,
            data=create_schema.data.json(),
            tracking_event_trigger_id=create_schema.tracking_event_trigger_id or None,
            schedule_trigger_id=create_schema.schedule_trigger_id or None,
        )

    @classmethod
    def as_schema_model(cls, database_model: any, **kwargs):
        import json

        try:
            database_model.data = json.loads(database_model.data)
        except TypeError:
            database_model.data = database_model.data
        return cls.schema_model().from_orm(database_model)

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(action=schema_model)

    @classmethod
    def send_trigger_notification(cls, notification_id, event_id, trigger_type):
        if trigger_type == TrackingEventTrigger.ON_DONE.type:
            pass

    @classmethod
    def execute_trigger_event(cls, method, model_id, import_path):
        if import_path:
            exec(import_path)
            exec(f'{method}(model_id)')

    def __init__(self, action: ActionSchema):
        self.action = action

    @property
    def fields(self) -> ActionSchema:
        return self.action

    def run(self):
        data = self.fields.data

        if type(data) == ActionDataSchema:
            executable_method = data.method
            executable_method_args = data.args
        else:
            executable_method = data['method']
            executable_method_args = data['args']

        exec(f'self.{executable_method}(*executable_method_args)')
