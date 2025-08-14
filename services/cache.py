"""
Redis cache initialization utilities for FastAPI.

Configures a Redis client and sets up FastAPI-Cache with a Redis backend,
enabling response caching for API endpoints.
"""

import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

redis_client = redis.Redis(
        host="redis",
        port=6379,
        decode_responses=True
    )


async def init_cache():
    """
    Initialize FastAPI-Cache with Redis backend.

    Sets up caching for FastAPI endpoints using the configured Redis client.
    """

    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
