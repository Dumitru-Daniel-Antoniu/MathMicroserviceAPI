"""
Caching helpers for mathematical operation endpoints.

Provides Prometheus metrics for cache hits and misses, and an async handler
to retrieve or compute operation results using Redis caching and background
logging.
"""

from prometheus_client import Counter
from services.cache import redis_client
from database.database import log_request
from views.views import OperationView

cache_hits = Counter("cache_hits_total", "Cache hits per endpoint",
                     ["method", "endpoint"])
cache_misses = Counter("cache_misses_total", "Cache misses per endpoint",
                       ["method", "endpoint"])


async def handle_cached_operation(
    operation: str,
    key: str,
    endpoint: str,
    request,
    background_tasks,
    calc_func,
    result_type=float,
    expire: int = 60
):
    """
    Handle caching logic for a mathematical operation.

    Checks Redis for a cached result. If found, returns the cached value
    and increments cache hit metrics. If not found, computes the result,
    caches it, logs the request, and increments cache miss metrics.

    Args:
        operation (str): Name of the operation.
        key (str): Redis cache key.
        endpoint (str): API endpoint path.
        request: pydantic schema objects with input data.
        background_tasks: FastAPI background tasks manager.
        calc_func: Function to compute the result if not cached.
        result_type (type, optional): Type to cast the result.
                                      Defaults to float.
        expire (int, optional): Cache expiration in seconds.
                                Defaults to 60 seconds.

    Returns:
        OperationView: Result view containing operation name,
                       input, and result.
    """

    is_cached = await redis_client.exists(key)
    if is_cached:
        cache_hits.labels(
            method="POST",
            endpoint=endpoint
        ).inc()
        cached = await redis_client.get(key)
        return OperationView(
            operation=operation,
            input=request.model_dump(),
            result=result_type(cached)
        )
    else:
        cache_misses.labels(
            method="POST",
            endpoint=endpoint
        ).inc()
        result = calc_func()
        await redis_client.set(key, result, ex=expire)

        background_tasks.add_task(
            log_request,
            operation,
            request.model_dump(),
            result,
            endpoint
        )

        return OperationView(
            operation=operation,
            input=request.model_dump(),
            result=result_type(result)
        )
