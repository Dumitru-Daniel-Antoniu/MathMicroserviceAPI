from pydantic import BaseModel, Field


class User(BaseModel):
    """Schema for user data."""
    username: str = Field(..., description="Username of the user")
    disabled: bool = Field(default=False,
                           description="Indicates if the user is disabled")


class InternalUser(BaseModel):
    """Schema for user authentication."""
    username: str
    hashed_password: str = Field(
        ...,
        min_length=8,
        description="User's password with minimum length of 8 characters"
    )
    disabled: bool = False


class TokenData(BaseModel):
    """Schema for token data."""
    username: str | None = None


class LoginRequest(BaseModel):
    """Request schema for user login."""
    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")


class LoginResponse(BaseModel):
    """Response schema for user login."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token")


class PowRequest(BaseModel):
    """Request schema for power operation."""
    base: int = Field(..., description="Base number")
    exponent: int = Field(..., description="Exponent")


class LogRequest(BaseModel):
    """Request schema for logarithm operation."""
    n: int = Field(..., description="Input of the logarithm")
    base: int = Field(..., description="Base of the logarithm")


class SqrtRequest(BaseModel):
    """Request schema for square root operation."""
    n: int = Field(..., description="Input number")


class FibonacciRequest(BaseModel):
    """Request schema for Fibonacci operation."""
    n: int = Field(..., description="n-th Fibonacci number to calculate")


class FactorialRequest(BaseModel):
    """Request schema for factorial operation."""
    n: int = Field(..., description="Number to calculate factorial for")
