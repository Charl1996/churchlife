from app.integrations.messaging.messaging_platform import MessagingPlatform, MESSAGING_PLATFORM_TYPE
from app.requests import (
    get_request
)
from app.integrations.platform_schema import PlatformSchema


class RespondIOMessagingPlatform(MessagingPlatform):

    slug = 'respondio'
    example_api_url = 'https://app.respond.io/api/v1'

    platform: PlatformSchema

    @classmethod
    def test_connection(cls, configuration):
        api_key = configuration['api_key']

        # Need some more configuration to let users manage tags
        test_url = f'{cls.example_api_url}/contact/by_custom_field?name=active&value=true&page=1'
        status_code, content, errors = get_request(test_url, headers=cls.headers(api_key))

        if content.get('status', '') == 'error':
            errors = content.get('message', '')

        if errors:
            if isinstance(errors, list):
                error_message = errors[0]
            else:
                error_message = errors

            return 403, error_message

        return status_code, None

    @classmethod
    def schema_model(cls):
        return PlatformSchema

    @classmethod
    def create_schema_model(cls):
        return PlatformSchema

    @classmethod
    def create_model(cls, create_schema: PlatformSchema):
        return cls.database_model()(
            slug=cls.slug,
            api_key=create_schema.api_key,
            organisation_id=create_schema.organisation_id,
            type=MESSAGING_PLATFORM_TYPE,
        )

    @classmethod
    def headers(cls, api_key):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    @classmethod
    def init_class_instance(cls, schema_model):
        return cls(platform=schema_model)

    def __init__(self, platform: PlatformSchema):
        self.platform = platform

    @property
    def fields(self) -> PlatformSchema:
        return self.platform
