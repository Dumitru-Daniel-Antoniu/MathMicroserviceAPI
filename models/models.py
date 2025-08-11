from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class OperationLog(Base):
    """Model for logging mathematical operations."""
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
    """Model for user authentication."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
