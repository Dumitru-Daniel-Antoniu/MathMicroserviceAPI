from pydantic import BaseModel, Field

class OperationView(BaseModel):
    operation: str = Field(..., description="Operation performed")
    input: dict = Field(..., description="Input values")
    result: float = Field(..., description="Result of the operation")