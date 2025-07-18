from pydantic import BaseModel, Field

class PowRequest(BaseModel):
    """Request schema for power operation."""
    base: int = Field(..., description="Base number")
    exponent: int = Field(..., description="Exponent")

class LogRequest(BaseModel):
    """Request schema for logarithm operation."""
    input: int = Field(..., description="Input of the logarithm")
    base: int = Field(..., description="Base of the logarithm")

class SqrtRequest(BaseModel):
    """Request schema for square root operation."""
    input: int = Field(..., description="Input number")

class FibonacciRequest(BaseModel):
    """Request schema for Fibonacci operation."""
    n: int = Field(..., description="n-th Fibonacci number to calculate")

class FactorialRequest(BaseModel):
    """Request schema for factorial operation."""
    n: int = Field(..., description="Number to calculate factorial for")

class MathResponse(BaseModel):
    """Response schema for mathematical operations."""
    operation: str = Field(..., description="Operation performed")
    input: dict = Field(..., description="Input values")
    result: float = Field(..., description="Result of the operation")
