from fastapi import APIRouter, BackgroundTasks
from schemas import PowRequest, FibonacciRequest, FactorialRequest, SqrtRequest, LogRequest, MathResponse
from math_services import power, fibonacci, factorial, sqrt, logarithm
from database import log_request

router = APIRouter()

@router.post("/pow", response_model=MathResponse)
async def calculate_pow(request: PowRequest, background_tasks: BackgroundTasks):
    # controller logic: calls service and orchestrates logging
    result = power(request.base, request.exponent)
    background_tasks.add_task(log_request, "pow", request.dict(), result)

    # view logic: formats response
    return MathResponse(operation="pow", input=request.dict(), result=result)

@router.post("/sqrt", response_model=MathResponse)
async def calculate_sqrt(request: SqrtRequest, background_tasks: BackgroundTasks):
    # controller logic: calls service and orchestrates logging
    result = sqrt(request.input)
    background_tasks.add_task(log_request, "sqrt", request.dict(), result)

    # view logic: formats response
    return MathResponse(operation="sqrt", input=request.dict(), result=result)

@router.post("/log", response_model=MathResponse)
async def calculate_log(request: LogRequest, background_tasks: BackgroundTasks):
    # controller logic: calls service and orchestrates logging
    result = logarithm(request.input, request.base)
    background_tasks.add_task(log_request, "log", request.dict(), result)

    # view logic: formats response
    return MathResponse(operation="log", input=request.dict(), result=result)

@router.post("/fibonacci", response_model=MathResponse)
async def calculate_fibonacci(request: FibonacciRequest, background_tasks: BackgroundTasks):
    # controller logic: calls service and orchestrates logging
    result = fibonacci(request.n)
    background_tasks.add_task(log_request, "fibonacci", request.dict(), result)

    # view logic: formats response
    return MathResponse(operation="fibonacci", input=request.dict(), result=result)

@router.post("/factorial", response_model=MathResponse)
async def calculate_factorial(request: FactorialRequest, background_tasks: BackgroundTasks):
    # controller logic: calls service and orchestrates logging
    result = factorial(request.n)
    background_tasks.add_task(log_request, "factorial", request.dict(), result)

    # view logic: formats response
    return MathResponse(operation="factorial", input=request.dict(), result=result)