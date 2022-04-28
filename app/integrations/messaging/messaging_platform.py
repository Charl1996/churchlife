from app.database.interface import DatabaseInterfaceWrapper
from app.integrations.platform_schema import PlatformSchema
from app.database.models import Platform as PlatformModel


MESSAGING_PLATFORM_TYPE = 'messaging'

"""
This class is a generic messaging platform implementation that all
subclasses should adhere to
"""


class MessagingPlatform(DatabaseInterfaceWrapper):

    @classmethod
    def database_model(cls):
        return PlatformModel

    @classmethod
    def schema_model(cls):
        return PlatformSchema

    @classmethod
    def create_schema_model(cls):
        return PlatformSchema

    def get_people(self):
        raise NotImplementedError

    @classmethod
    def test_connection(cls, configuration):
        raise NotImplementedError

    @classmethod
    def linked_to_organisation(cls, organisation_id, slug, api_key):
        res = cls.get_by(criteria={
            'organisation_id': organisation_id,
            'slug': slug,
            'api_key': api_key,
            'type': MESSAGING_PLATFORM_TYPE,
        })
        return False if not res else True

    @classmethod
    def get_by_slug(cls, slug):
        if slug == 'respondio':
            from app.integrations.messaging.respondio_platform import RespondIOMessagingPlatform
            return RespondIOMessagingPlatform

        return None

    @classmethod
    def create_platform(cls, platform, configuration):
        # Avoid circular imports
        from app.integrations.messaging.respondio_platform import RespondIOMessagingPlatform

        platform_obj = None

        if platform == RespondIOMessagingPlatform.slug:
            configuration['slug'] = RespondIOMessagingPlatform.slug
            configuration['type'] = MESSAGING_PLATFORM_TYPE
            platform_obj = RespondIOMessagingPlatform.create(configuration)

        return platform_obj
