from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, OperationLog

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Initiates database connection
async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Function to log requests
async def log_request(operation: str, input_data: dict, result: float):
    async with SessionLocal() as session:
        log_entry = OperationLog(
            operation=operation,
            input=str(input_data),
            result=result
        )
        session.add(log_entry)
        await session.commit()
