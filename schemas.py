from pydantic import BaseModel, Field

class OperationRequest(BaseModel):
    operation: str = Field(..., description="The mathematical operation to perform")
    a: float = Field(..., description="The first operand")
    b: float = Field(..., description="The second operand")

class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")
    message: str = Field(..., description="A message indicating success or failure")
