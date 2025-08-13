from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from schemas.schemas import PowRequest, FibonacciRequest, \
                            FactorialRequest, SqrtRequest, LogRequest, User, \
                            LoginRequest, LoginResponse
from services.math_services import power, fibonacci, factorial, sqrt, logarithm
from database.database import log_request
from services.auth import get_current_user, create_access_token, \
                            authenticate_user, create_user
import time

from views.views import OperationView
from helpers.cache_helpers import handle_cached_operation
from services.logging_utils import log_to_redis_stream

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK, tags=["Authentication"])
async def login(form_data: LoginRequest):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    result = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    result.set_cookie(key="access_token", value=access_token, httponly=True)
    return result

@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register(form_data: LoginRequest):
    user = await create_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    access_token = create_access_token(data={"sub": user.username})
    result = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    result.set_cookie(key="access_token", value=access_token, httponly=True)
    return result

@router.get("/logout", response_model=OperationView, tags=["Authentication"])
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@router.get("/userinfo", tags=["User Info"])
def get_user_info(user: User = Depends(get_current_user)):
    return JSONResponse(
        content={
            "username": user.username,
            "disabled": user.disabled
        }
    )

@router.post("/pow", response_model=OperationView, tags=["Mathematical Operations"])
async def calculate_pow(
    request: PowRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    try:
        key = f"pow:{request.base}:{request.exponent}"
        endpoint = f"/pow?base={request.base}&exponent={request.exponent}"
        result = power(request.base, request.exponent)
        await log_request("pow", request.model_dump(), result)
        return await handle_cached_operation(
            "pow", key, endpoint, request, background_tasks,
            lambda: power(request.base, request.exponent), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sqrt", response_model=OperationView, tags=["Mathematical Operations"])
async def calculate_sqrt(request: SqrtRequest,
                         background_tasks: BackgroundTasks,
                         user: User = Depends(get_current_user)):
    try:
        key = f"sqrt:{request.input}"
        endpoint = f"/sqrt?input={request.input}"
        result = sqrt(request.input)
        await log_request("sqrt", request.model_dump(), result)
        return await handle_cached_operation(
            "sqrt", key, endpoint, request, background_tasks,
            lambda: sqrt(request.input), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/log", response_model=OperationView, tags=["Mathematical Operations"])
async def calculate_log(request: LogRequest,
                        background_tasks: BackgroundTasks,
                        user: User = Depends(get_current_user)):
    try:
        key = f"log:{request.input}:{request.base}"
        endpoint = f"/log?input={request.input}&base={request.base}"
        result = logarithm(request.input, request.base)
        await log_request("log", request.model_dump(), result)
        return await handle_cached_operation(
            "log", key, endpoint, request, background_tasks,
            lambda: logarithm(request.input, request.base), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=OperationView, tags=["Mathematical Operations"])
async def calculate_fibonacci(request: FibonacciRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        key = f"fibonacci:{request.n}"
        endpoint = f"/fibonacci?n={request.n}"
        result = fibonacci(request.n)
        await log_request("fibonacci", request.model_dump(), result)
        return await handle_cached_operation(
            "fibonacci", key, endpoint, request, background_tasks,
            lambda: fibonacci(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=OperationView, tags=["Mathematical Operations"])
async def calculate_factorial(request: FactorialRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        key = f"factorial:{request.n}"
        endpoint = f"/factorial?n={request.n}"
        result = factorial(request.n)
        await log_request("factorial", request.model_dump(), result)
        return await handle_cached_operation(
            "factorial", key, endpoint, request, background_tasks,
            lambda: factorial(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test-redis")
def test_redis():
    log_to_redis_stream({"manual": "test", "source": "test-kafka route"})
    time.sleep(1)  # Give some time for the message to be processed
    return {"status": "test message sent"}