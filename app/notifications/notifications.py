import json

from collections import namedtuple
from app.database import (
    Notification as NotificationModel,
    NotificationItem as NotificationItemModel,
)
from app.notifications import (
    NotificationSchema,
    NotificationCreateSchema,
    NotificationItemSchema,
)
from app.database.interface import DatabaseInterfaceWrapper
from app.notifications.exceptions import (
    UnsupportedNotificationTypeError,
    MissingNotificationDataError,
)


class Notification(DatabaseInterfaceWrapper):

    notification: NotificationSchema

    @classmethod
    def database_model(cls):
        return NotificationModel

    @classmethod
    def create_schema_model(cls):
        return NotificationCreateSchema

    @classmethod
    def schema_model(cls):
        return NotificationSchema

    @classmethod
    def create_model(cls, create_schema: NotificationCreateSchema):
        return NotificationModel(
            name=create_schema.name,
            organisation_id=create_schema.organisation_id,
        )

    @classmethod
    def get_by_id(cls, notification_id: str):
        schema_obj = super().get_by(field='id', value=notification_id)
        return cls(notification=schema_obj)

    @classmethod
    def notify_event_trigger(cls, notification_id, trigger_type):
        pass

    @classmethod
    def delete(cls, model_id: str):
        NotificationItem.delete_where(
            criteria={'notification_id': model_id},
        )
        super().delete(model_id=model_id)

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(notification=schema_model)

    def __init__(self, notification: NotificationSchema):
        self.notification = notification

    @property
    def fields(self) -> NotificationSchema:
        return self.notification

    def add_notification_item(self, item_type: str, data: any):
        NotificationItem.create({
            'type': item_type,
            'data': data,
            'notification_id': self.fields.id,
        })

    def get_notification_items(self):
        return NotificationItem.get_by_notification_id(
            notification_id=self.fields.id,
        )


NotificationType = namedtuple('NotificationType', ('type', 'data_keys'))


class NotificationItem(DatabaseInterfaceWrapper):

    EMAIL = NotificationType(type='email', data_keys=['email'])

    SUPPORTED_NOTIFICATION_TYPES = [
        EMAIL,
    ]

    notification_item: NotificationItemSchema

    @classmethod
    def database_model(cls):
        return NotificationItemModel

    @classmethod
    def create_schema_model(cls):
        return NotificationItemSchema

    @classmethod
    def schema_model(cls):
        return NotificationItemSchema

    @classmethod
    def create_model(cls, create_schema: NotificationItemSchema):
        supported_type = next((t for t in cls.SUPPORTED_NOTIFICATION_TYPES if t.type == create_schema.type))

        if not supported_type:
            raise UnsupportedNotificationTypeError(f'Unsupported notification type: {create_schema.type}')

        missing_data_keys = cls.validate_notification_type_data(supported_type.data_keys, create_schema.data.keys())

        if missing_data_keys:
            raise MissingNotificationDataError(f'Missing data {missing_data_keys} for {create_schema.type}')

        return NotificationItemModel(
            type=create_schema.type,
            data=create_schema.data,
            notification_id=create_schema.notification_id,
        )

    @classmethod
    def get_by_notification_id(cls, notification_id: str):
        schema_objs = super().get_all_by(criteria={'notification_id': notification_id})
        return [cls(notification_item=schema_obj) for schema_obj in schema_objs]

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(notification_item=schema_model)

    def __init__(self, notification_item: NotificationItemSchema):
        self.notification_item = notification_item

    @classmethod
    def validate_notification_type_data(cls, required_keys: any, data_keys: any):
        return set(required_keys).difference(set(data_keys))

    def __init__(self, notification_item: NotificationItemSchema):
        self.notification_item = notification_item

    @property
    def fields(self) -> NotificationItemSchema:
        return self.notification_item
