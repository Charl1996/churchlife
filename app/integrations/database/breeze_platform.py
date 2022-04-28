from app.integrations.database.database_platform import DatabasePlatform, DATABASE_PLATFORM_TYPE
from app.requests import (
    get_request
)
from app.integrations.database.database_platform_schema import (
    BreezePlatformSchema
)


class BreezeDatabasePlatform(DatabasePlatform):

    slug = 'breeze'
    subdomain_placeholder = '<subdomain>'
    example_api_url = f'https://{subdomain_placeholder}.breezechms.com/api'

    platform: BreezePlatformSchema

    @classmethod
    def test_connection(cls, configuration):
        subdomain = configuration['subdomain']
        test_base_url = cls.example_api_url.replace(cls.subdomain_placeholder, subdomain)
        api_key = configuration['api_key']

        test_url = f'{test_base_url}/people?limit=1'
        status_code, _content, errors = get_request(test_url, headers=cls.headers(api_key))

        if errors:
            if isinstance(errors, list):
                error_message = errors[0]
            else:
                error_message = errors

            return 403, error_message

        return status_code, None

    @classmethod
    def schema_model(cls):
        return BreezePlatformSchema

    @classmethod
    def create_schema_model(cls):
        return BreezePlatformSchema

    @classmethod
    def create_model(cls, create_schema: BreezePlatformSchema):
        return cls.database_model()(
            slug=cls.slug,
            subdomain=create_schema.subdomain,
            api_key=create_schema.api_key,
            organisation_id=create_schema.organisation_id,
            type=DATABASE_PLATFORM_TYPE,
        )

    @classmethod
    def headers(cls, api_key):
        return {
            'Content-Type': 'application/json',
            'Api-Key': f'{api_key}'
        }

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(platform=schema_model)

    def __init__(self, platform: BreezePlatformSchema):
        self.platform = platform

    @property
    def fields(self) -> BreezePlatformSchema:
        return self.platform

    def get_people(self):
        pass
