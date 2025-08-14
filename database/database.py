"""
Database session management and logging utilities for FastAPI application.

Provides asynchronous SQLAlchemy engine and session creation,
database initialization, and functions to log operations and user requests
to both the database and Redis stream.
"""

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
    """
    Initialize database tables if they do not exist.

    Runs SQLAlchemy metadata creation in an async context.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def log_request(operation: str, input_data: dict,
                      result: float, path: str):
    """
    Log a mathematical operation to the database and Redis stream.

    Args:
        operation (str): Name of the operation performed.
        input_data (dict): Input parameters for the operation.
        result (float): Result of the operation.
        path (str): API endpoint path.

    Logs the operation to the database and sends a structured
    log entry to Redis.
    """

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
    """
    Log a user-related request to Redis stream.

    Args:
        username (str): Username of the user.
        disabled (bool): User's disabled status.
        method (str): HTTP method used.
        path (str): API endpoint path.

    Sends a structured log entry to Redis.
    """

    payload = {
        "username": username,
        "disabled": disabled
    }
    log_entry = {
        "method": method,
        "path": path,
        "payload": payload
    }
    try:
        log_to_redis_stream(log_entry)
        print(f"User creation logged to Redis Stream: {log_entry}")
    except Exception as e:
        print(f"Error logging to Redis Stream: {e}")


async def get_request(path: str):
    """
    Log a GET request to Redis stream.

    Args:
        path (str): API endpoint path.

    Sends a GET request log entry to Redis and prints the result.
    """

    log_entry = {
        "method": "GET",
        "path": path
    }
    try:
        log_to_redis_stream(log_entry)
        print(f"Get request logged to Redis Stream: {log_entry}")
    except Exception as e:
        print(f"Error logging to Redis Stream: {e}")
