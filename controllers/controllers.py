"""
API route definitions for authentication, user info
and mathematical operations.

This module provides FastAPI endpoints for:
- User authentication (login, register, logout)
- Retrieving user information
- Performing mathematical operations
  (power, square root, logarithm, Fibonacci, factorial)
- Testing Redis logging integration

Endpoints use dependency injection for authentication and background tasks,
and leverage caching and logging utilities for efficient operation handling.
"""

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
    """
    Authenticate a user and return a JWT access token.

    Args:
        form_data (LoginRequest): User login credentials.

    Returns:
        JSONResponse: Access token and token type in response.

    Raises:
        HTTPException: If credentials are invalid.
    """

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
    """
    Register a new user and return a JWT access token.

    Args:
        form_data (LoginRequest): New user credentials.

    Returns:
        JSONResponse: Access token and token type in response.

    Raises:
        HTTPException: If user already exists.
    """

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
    """
    Log out the current user by deleting the access token cookie.

    Returns:
        RedirectResponse: Redirects to the login/register page.
    """

    await get_request("/logout")
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/userinfo", tags=["User Info"])
async def get_user_info(user: User = Depends(get_current_user)):
    """
    Retrieve information about the current authenticated user.

    Args:
        user (User): The authenticated user (dependency).

    Returns:
        JSONResponse: User info including username and disabled status.
    """

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
    """
    Calculate the power of a base raised to an exponent.

    Args:
        request (PowRequest): Base and exponent values.
        background_tasks (BackgroundTasks): FastAPI background tasks.
        user (User): The authenticated user (dependency).

    Returns:
        OperationView: Result of the power operation.

    Raises:
        HTTPException: If calculation fails.
    """

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
    """
    Calculate the square root of a number.

    Args:
        request (SqrtRequest): Number to calculate the square root of.
        background_tasks (BackgroundTasks): FastAPI background tasks.
        user (User): The authenticated user (dependency).

    Returns:
        OperationView: Result of the square root operation.

    Raises:
        HTTPException: If calculation fails.
    """

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
    """
    Calculate the logarithm of a number with a given base.

    Args:
        request (LogRequest): Number and base for the logarithm.
        background_tasks (BackgroundTasks): FastAPI background tasks.
        user (User): The authenticated user (dependency).

    Returns:
        OperationView: Result of the logarithm operation.

    Raises:
        HTTPException: If calculation fails.
    """

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
    """
    Calculate the n-th Fibonacci number.

    Args:
        request (FibonacciRequest): The position in the Fibonacci sequence.
        background_tasks (BackgroundTasks): FastAPI background tasks.
        user (User): The authenticated user (dependency).

    Returns:
        OperationView: Result of the Fibonacci calculation.

    Raises:
        HTTPException: If calculation fails.
    """

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
    """
    Calculate the factorial of a number.

    Args:
        request (FactorialRequest): Number to calculate the factorial of.
        background_tasks (BackgroundTasks): FastAPI background tasks.
        user (User): The authenticated user (dependency).

    Returns:
        OperationView: Result of the factorial operation.

    Raises:
        HTTPException: If calculation fails.
    """

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
    """
    Send a test log message to Redis for integration testing.

    Returns:
        dict: Status of the test message.
    """

    log_to_redis_stream({"manual": "test", "source": "test-kafka route"})
    time.sleep(1)
    return {"status": "test message sent"}
