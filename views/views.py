"""
View models for mathematical operation responses in FastAPI.

Defines Pydantic models for representing operation details,
inputs, and results returned by API endpoints.
"""

from pydantic import BaseModel, Field


class OperationView(BaseModel):
    """
    View for mathematical operations.

    Attributes:
        operation (str): Operation performed.
        input (dict): Input values for the operation.
        result (float): Result of the operation.
    """

    operation: str = Field(..., description="Operation performed")
    input: dict = Field(..., description="Input values")
    result: float = Field(..., description="Result of the operation")
