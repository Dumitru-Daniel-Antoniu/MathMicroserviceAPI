"""
SQLAlchemy ORM models for user accounts and mathematical operation logs.

Defines database tables for storing user credentials and operation history,
including operation type, input, result, and timestamp.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class OperationLog(Base):
    """
    ORM model for logging mathematical operations.

    Attributes:
        id (int): Primary key.
        operation (str): Name of the operation performed.
        input (str): Input parameters as string.
        result (float): Result of the operation.
        timestamp (datetime): Time when the operation was logged.
    """

    __tablename__ = 'operation_log'

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    input = Column(String, index=True)
    result = Column(Float, index=True)
    timestamp = Column(DateTime(timezone=True),
                       default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"""<OperationLog(id={self.id},
        operation='{self.operation}',
        input='{self.input}',
        result={self.result},
        timestamp='{self.timestamp}')>"""


class User(Base):
    """
    ORM model for user accounts.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        hashed_password (str): Hashed user password.
        disabled (bool): User's disabled status.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
