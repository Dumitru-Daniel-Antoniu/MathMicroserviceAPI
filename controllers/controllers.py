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
from services.auth import get_current_user, create_access_token, authenticate_user

router = APIRouter()

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(form_data: LoginRequest):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
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
        background_tasks.add_task(
            log_request,
            "pow",
            request.model_dump(),
            result
        )
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
                         background_tasks: BackgroundTasks):
    try:
        result = sqrt(request.input)
        background_tasks.add_task(
            log_request,
            "sqrt",
            request.model_dump(),
            result
        )
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
                        background_tasks: BackgroundTasks):
    try:
        result = logarithm(request.input, request.base)
        background_tasks.add_task(
            log_request,
            "log",
            request.model_dump(),
            result
        )
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
                              background_tasks: BackgroundTasks):
    try:
        result = fibonacci(request.n)
        background_tasks.add_task(
            log_request,
            "fibonacci",
            request.model_dump(),
            result
        )
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
                              background_tasks: BackgroundTasks):
    try:
        result = factorial(request.n)
        background_tasks.add_task(
            log_request,
            "factorial",
            request.model_dump(),
            result
        )
        return OperationView(
            operation="factorial",
            input=request.model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
