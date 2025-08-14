import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

redis_client = redis.Redis(
        host="redis",
        port=6379,
        decode_responses=True
    )


async def init_cache():
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
