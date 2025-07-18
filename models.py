from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class OperationLog(Base):
    """Model for logging mathematical operations."""
    __tablename__ = 'operation_log'

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    input = Column(String, index=True)
    result = Column(Float, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<OperationLog(id={self.id}, operation='{self.operation}', timestamp='{self.timestamp}')>"
    