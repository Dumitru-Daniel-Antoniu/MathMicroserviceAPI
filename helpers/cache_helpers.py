from prometheus_client import Counter
from services.cache import redis_client
from database.database import log_request
from views.views import OperationView

cache_hits = Counter("cache_hits_total", "Cache hits per endpoint", ["method", "endpoint"])
cache_misses = Counter("cache_misses_total", "Cache misses per endpoint", ["method", "endpoint"])

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