from fastapi import APIRouter, BackgroundTasks, HTTPException
from views import OperationView
from schemas import PowRequest, FibonacciRequest, FactorialRequest, SqrtRequest, LogRequest
from math_services import power, fibonacci, factorial, sqrt, logarithm
from database import log_request

router = APIRouter()

@router.post("/pow", response_model=OperationView)
async def calculate_pow(request: PowRequest, background_tasks: BackgroundTasks):
    try:
        result = power(request.base, request.exponent)
        background_tasks.add_task(log_request, "pow", request.model_dump(), result)
        return OperationView(operation="pow", input=request.model_dump(), result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sqrt", response_model=OperationView)
async def calculate_sqrt(request: SqrtRequest, background_tasks: BackgroundTasks):
    try:
        result = sqrt(request.input)
        background_tasks.add_task(log_request, "sqrt", request.model_dump(), result)
        return OperationView(operation="sqrt", input=request.model_dump(), result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/log", response_model=OperationView)
async def calculate_log(request: LogRequest, background_tasks: BackgroundTasks):
    try:
        result = logarithm(request.input, request.base)
        background_tasks.add_task(log_request, "log", request.model_dump(), result)
        return OperationView(operation="log", input=request.model_dump(), result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fibonacci", response_model=OperationView)
async def calculate_fibonacci(request: FibonacciRequest, background_tasks: BackgroundTasks):
    try:
        result = fibonacci(request.n)
        background_tasks.add_task(log_request, "fibonacci", request.model_dump(), result)
        return OperationView(operation="fibonacci", input=request.model_dump(), result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/factorial", response_model=OperationView)
async def calculate_factorial(request: FactorialRequest, background_tasks: BackgroundTasks):
    try:
        result = factorial(request.n)
        background_tasks.add_task(log_request, "factorial", request.model_dump(), result)
        return OperationView(operation="factorial", input=request.model_dump(), result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))