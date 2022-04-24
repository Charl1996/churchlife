from app.integrations.database.database_platform import DatabasePlatform


def test_database_platform_connection(platform, configuration):
    platform = DatabasePlatform.get_by_slug(platform)

    if not platform:
        return 422

    return platform.test_connection(configuration)
