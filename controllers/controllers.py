import time
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from schemas.schemas import PowRequest, FibonacciRequest, \
                            FactorialRequest, SqrtRequest, LogRequest, User, \
                            LoginRequest, LoginResponse
from services.math_services import power, fibonacci, factorial, sqrt, logarithm
from database.database import user_request, get_request
from services.auth import get_current_user, create_access_token, \
                            authenticate_user, create_user
from views.views import OperationView
from helpers.cache_helpers import handle_cached_operation
from services.logging_utils import log_to_redis_stream

router = APIRouter()


@router.post("/login", response_model=LoginResponse,
             status_code=status.HTTP_200_OK,
             tags=["Authentication"])
async def login(form_data: LoginRequest):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    await user_request(user.username, user.disabled, "POST", "/login")
    access_token = create_access_token(data={"sub": user.username})
    result = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    result.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax'
    )
    return result


@router.post("/register", response_model=LoginResponse,
             status_code=status.HTTP_201_CREATED,
             tags=["Authentication"])
async def register(form_data: LoginRequest):
    user = await create_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    await user_request(user.username, user.disabled, "POST", "/register")
    access_token = create_access_token(data={"sub": user.username})
    result = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    result.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax'
    )
    return result


@router.get("/logout", response_model=OperationView, tags=["Authentication"])
async def logout():
    await get_request("/logout")
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/userinfo", tags=["User Info"])
async def get_user_info(user: User = Depends(get_current_user)):
    await user_request(user.username, user.disabled, "GET", "/userinfo")
    return JSONResponse(
        content={
            "username": user.username,
            "disabled": user.disabled
        }
    )


@router.post("/pow", response_model=OperationView,
             tags=["Mathematical Operations"])
async def calculate_pow(
    request: PowRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user)
):
    try:
        key = f"pow:{request.base}:{request.exponent}"
        endpoint = f"/pow?base={request.base}&exponent={request.exponent}"
        return await handle_cached_operation(
            "pow", key, endpoint, request, background_tasks,
            lambda: power(request.base, request.exponent), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sqrt", response_model=OperationView,
             tags=["Mathematical Operations"])
async def calculate_sqrt(request: SqrtRequest,
                         background_tasks: BackgroundTasks,
                         user: User = Depends(get_current_user)):
    try:
        key = f"sqrt:{request.n}"
        endpoint = f"/sqrt?n={request.n}"
        return await handle_cached_operation(
            "sqrt", key, endpoint, request, background_tasks,
            lambda: sqrt(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/log", response_model=OperationView,
             tags=["Mathematical Operations"])
async def calculate_log(request: LogRequest,
                        background_tasks: BackgroundTasks,
                        user: User = Depends(get_current_user)):
    try:
        key = f"log:{request.n}:{request.base}"
        endpoint = f"/log?n={request.n}&base={request.base}"
        return await handle_cached_operation(
            "log", key, endpoint, request, background_tasks,
            lambda: logarithm(request.n, request.base), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=OperationView,
             tags=["Mathematical Operations"])
async def calculate_fibonacci(request: FibonacciRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        key = f"fibonacci:{request.n}"
        endpoint = f"/fibonacci?n={request.n}"
        return await handle_cached_operation(
            "fibonacci", key, endpoint, request, background_tasks,
            lambda: fibonacci(request.n), float
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=OperationView,
             tags=["Mathematical Operations"])
async def calculate_factorial(request: FactorialRequest,
                              background_tasks: BackgroundTasks,
                              user: User = Depends(get_current_user)):
    try:
        key = f"factorial:{request.n}"
        endpoint = f"/factorial?n={request.n}"
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
