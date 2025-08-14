"""
Pydantic schemas for user authentication, mathematical operation requests
and API responses.

Defines data models for user info, login, JWT tokens and requests
for power, square root, logarithm, Fibonacci, and factorial operations.
"""

from pydantic import BaseModel, Field


class User(BaseModel):
    """
    Schema for user information.

    Attributes:
        username (str): Username of the user.
        disabled (bool): Indicates if the user is disabled.
    """

    username: str = Field(..., description="Username of the user")
    disabled: bool = Field(default=False,
                           description="Indicates if the user is disabled")


class InternalUser(BaseModel):
    """
    Schema for internal user representation with hashed password.

    Attributes:
        username (str): Username of the user.
        hashed_password (str): User's hashed password (min length 8).
        disabled (bool): Indicates if the user is disabled.
    """

    username: str
    hashed_password: str = Field(
        ...,
        min_length=8,
        description="User's password with minimum length of 8 characters"
    )
    disabled: bool = False


class TokenData(BaseModel):
    """
    Schema for JWT token data.

    Attributes:
        username (str | None): Username extracted from the token.
    """

    username: str | None = None


class LoginRequest(BaseModel):
    """
    Schema for login request payload.

    Attributes:
        username (str): Username for login.
        password (str): Password for login.
    """

    username: str = Field(..., description="Username for login")
    password: str = Field(..., description="Password for login")


class LoginResponse(BaseModel):
    """
    Schema for login response containing JWT token.

    Attributes:
        access_token (str): JWT access token.
        token_type (str): Type of the token.
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Type of the token")


class PowRequest(BaseModel):
    """
    Schema for power operation request.

    Attributes:
        base (int): Base number.
        exponent (int): Exponent.
    """

    base: int = Field(..., description="Base number")
    exponent: int = Field(..., description="Exponent")


class LogRequest(BaseModel):
    """
    Schema for logarithm operation request.

    Attributes:
        n (int): Input of the logarithm.
        base (int): Base of the logarithm.
    """

    n: int = Field(..., description="Input of the logarithm")
    base: int = Field(..., description="Base of the logarithm")


class SqrtRequest(BaseModel):
    """
    Schema for square root operation request.

    Attributes:
        n (int): Number to calculate square root for.
    """

    n: int = Field(..., description="Input number")


class FibonacciRequest(BaseModel):
    """
    Schema for Fibonacci operation request.

    Attributes:
        n (int): n-th Fibonacci number to calculate.
    """

    n: int = Field(..., description="n-th Fibonacci number to calculate")


class FactorialRequest(BaseModel):
    """
    Schema for factorial operation request.

    Attributes:
        n (int): Number to calculate factorial for.
    """

    n: int = Field(..., description="Number to calculate factorial for")
