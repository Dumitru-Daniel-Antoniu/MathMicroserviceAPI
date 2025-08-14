from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.models import Base, OperationLog
from services.logging_utils import log_to_redis_stream

DATABASE_URL = "sqlite+aiosqlite:///./info.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal: sessionmaker[AsyncSession] = sessionmaker(bind=engine,
                                                        class_=AsyncSession,
                                                        expire_on_commit=False)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def log_request(operation: str, input_data: dict,
                      result: float, path: str):
    async with SessionLocal() as session:
        log_entry = OperationLog(
            operation=operation,
            input=str(input_data),
            result=result
        )
        session.add(log_entry)
        await session.commit()

    payload = {
        "operation": operation,
        "input": str(input_data),
        "result": result
    }
    log_entry = {
        "method": "POST",
        "path": path,
        "payload": payload
    }
    try:
        log_to_redis_stream(log_entry)
        print(f"Logged to Redis Stream: {log_entry}")
    except Exception as e:
        print(f"Error logging to Redis Stream: {e}")


async def user_request(username: str, disabled: bool, method: str, path: str):
    payload = {
        "username": username,
        "disabled": disabled
    }
    log_entry = {
        "method": method,
        "path": path,
        "payload": payload
    }
    log_to_redis_stream(log_entry)


async def get_request(path: str):
    log_entry = {
        "method": "GET",
        "path": path
    }
    try:
        log_to_redis_stream(log_entry)
        print(f"User creation logged to Redis Stream: {log_entry}")
    except Exception as e:
        print(f"Error logging to Redis Stream: {e}")
