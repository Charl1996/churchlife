from app.integrations.database.database_platform import DatabasePlatform
from app.integrations.messaging.messaging_platform import MessagingPlatform


def test_database_platform_connection(platform, configuration):
    platform = DatabasePlatform.get_by_slug(platform)

    if not platform:
        return 422

    return platform.test_connection(configuration)


def test_messaging_platform_connection(platform, configuration):
    platform = MessagingPlatform.get_by_slug(platform)

    if not platform:
        return 422

    return platform.test_connection(configuration)
