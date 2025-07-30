from fastapi import APIRouter, BackgroundTasks, HTTPException

from schemas.schemas import PowRequest, FibonacciRequest, \
                            FactorialRequest, SqrtRequest, LogRequest
from services.math_services import power, fibonacci, factorial, sqrt, logarithm
from prometheus_client import Counter

from views.views import OperationView
from helpers.cache_helpers import handle_cached_operation

router = APIRouter()

@router.post("/pow", response_model=OperationView)
async def calculate_pow(
    request: PowRequest,
    background_tasks: BackgroundTasks
):
    try:
        key = f"pow:{request.base}:{request.exponent}"
        endpoint = f"/pow?base={request.base}&exponent={request.exponent}"
        return await handle_cached_operation(
            "pow", key, endpoint, request, background_tasks,
            lambda: power(request.base, request.exponent), float
        )
    except Exception as e:
        print("Cache key builder error: ", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sqrt", response_model=OperationView)
async def calculate_sqrt(
        request: SqrtRequest,
        background_tasks: BackgroundTasks
):
    try:
        key = f"sqrt:{request.input}"
        endpoint = f"/sqrt?input={request.input}"
        return await handle_cached_operation(
            "sqrt", key, endpoint, request, background_tasks,
            lambda: sqrt(request.input), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/log", response_model=OperationView)
async def calculate_log(
        request: LogRequest,
        background_tasks: BackgroundTasks
):
    try:
        key = f"log:{request.input}:{request.base}"
        endpoint = f"/log?input={request.input}&base={request.base}"
        return await handle_cached_operation(
            "log", key, endpoint, request, background_tasks,
            lambda: logarithm(request.input, request.base), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=OperationView)
async def calculate_fibonacci(
        request: FibonacciRequest,
        background_tasks: BackgroundTasks
):
    try:
        key = f"fibonacci:{request.n}"
        endpoint = f"/fibonacci?n={request.n}"
        return await handle_cached_operation(
            "fibonacci", key, endpoint, request, background_tasks,
            lambda: fibonacci(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=OperationView)
async def calculate_factorial(
        request: FactorialRequest,
        background_tasks: BackgroundTasks
):
    try:
        key = f"factorial:{request.n}"
        endpoint = f"/factorial?n={request.n}"
        return await handle_cached_operation(
            "factorial", key, endpoint, request, background_tasks,
            lambda: factorial(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
