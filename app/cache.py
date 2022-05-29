from fastapi_cache.backends.redis import CACHE_KEY
from fastapi_cache import caches

DATABASE_ENTITIES_CACHE_KEY = 'database-entities'


def redis_cache():
    return caches.get(CACHE_KEY)
