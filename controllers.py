from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import OperationRequest, OperationResponse
from database import SessionLocal
from models import OperationLog
from math_services import *

router = APIRouter(prefix='/api')

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/operation_log", response_model=OperationResponse)
async def math_operation_log(
    operation_log: OperationRequest,
    db: AsyncSession = Depends(get_db)
):
    if operation_log == "pow":
        result = power(operation_log.a, operation_log.b)
    elif operation_log.operation == "sqrt":
        result = square_root(operation_log.a)
    elif operation_log.operation == "log":
        if operation_log.b is None:
            result = logarithm(operation_log.a)
        else:
            result = logarithm(operation_log.a, operation_log.b)
    elif operation_log.operation == "factorial":
        result = factorial(operation_log.a)
    elif operation_log.operation == "fibonacci":
        result = fibonacci(operation_log.a)
    else:
        raise HTTPException(status_code=400, detail="Invalid/unsupported operation")
    
    log_entry = OperationLog(
        operation=operation_log.operation,
        input=f"{operation_log.a}, {operation_log.b}" if operation_log.b is not None else f"{operation_log.a}",
        result=result
    )
    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)
    
    return {'result': result, 'message': 'Operation successful'}