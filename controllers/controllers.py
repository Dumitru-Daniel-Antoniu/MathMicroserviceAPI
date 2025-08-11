from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from views.views import OperationView
from schemas.schemas import PowRequest, FibonacciRequest, \
                            FactorialRequest, SqrtRequest, LogRequest, User, \
                            LoginRequest, LoginResponse
from services.math_services import power, fibonacci, factorial, sqrt, logarithm
from database.database import log_request
from fastapi_cache.decorator import cache
from services.auth import get_current_user, create_access_token, \
                            authenticate_user, create_user
import time

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
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

@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/logout", response_class=OperationView)
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@router.get("/userinfo")
def get_user_info(user: User = Depends(get_current_user)):
    return JSONResponse(
        content={
            "username": user.username,
            "disabled": user.disabled
        }
    )

@router.post("/pow", response_model=OperationView)
@cache(expire=60)
async def calculate_pow(
    request: PowRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    try:
        result = power(request.base, request.exponent)
        await log_request("pow", request.model_dump(), result)
        return OperationView(
            operation="pow",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sqrt", response_model=OperationView)
@cache(expire=60)
async def calculate_sqrt(request: SqrtRequest,
                         background_tasks: BackgroundTasks,
                         user: User = Depends(get_current_user)):
    try:
        result = sqrt(request.input)
        await log_request("sqrt", request.model_dump(), result)
        return OperationView(
            operation="sqrt",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/log", response_model=OperationView)
@cache(expire=60)
async def calculate_log(request: LogRequest,
                        background_tasks: BackgroundTasks,
                        user: User = Depends(get_current_user)):
    try:
        result = logarithm(request.input, request.base)
        await log_request("log", request.model_dump(), result)
        return OperationView(
            operation="log",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=OperationView)
@cache(expire=60)
async def calculate_fibonacci(request: FibonacciRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        result = fibonacci(request.n)
        await log_request("fibonacci", request.model_dump(), result)
        return OperationView(
            operation="fibonacci",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=OperationView)
@cache(expire=60)
async def calculate_factorial(request: FactorialRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        result = factorial(request.n)
        await log_request("factorial", request.model_dump(), result)
        return OperationView(
            operation="factorial",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test-redis")
def test_redis():
    from services.logging_utils import log_to_redis_stream
    log_to_redis_stream({"manual": "test", "source": "test-kafka route"})
    time.sleep(1)  # Give some time for the message to be processed
    return {"status": "test message sent"}