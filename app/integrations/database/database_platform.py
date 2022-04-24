from app.database.interface import DatabaseInterfaceWrapper
from app.integrations.platform_schema import PlatformSchema
from app.database.models import Platform as PlatformModel

"""
This class is a generic database platform implementation that all
subclasses should adhere to
"""


class DatabasePlatform(DatabaseInterfaceWrapper):

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
        })
        return False if not res else True

    @classmethod
    def get_by_slug(cls, slug):
        if slug == 'breeze':
            from app.integrations.database.breeze_platform import BreezeDatabasePlatform
            return BreezeDatabasePlatform

        return None

    @classmethod
    def create_database_platform(cls, platform, configuration):
        # Avoid circular imports
        from app.integrations.database.breeze_platform import BreezeDatabasePlatform

        platform_obj = None

        if platform == BreezeDatabasePlatform.slug:
            configuration['slug'] = BreezeDatabasePlatform.slug
            platform_obj = BreezeDatabasePlatform.create(configuration)

        return platform_obj
