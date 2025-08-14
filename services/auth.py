"""
Authentication and user management services for
FastAPI application.

Handles password hashing, JWT token creation and verification,
user authentication, and user creation using SQLAlchemy
async sessions.
"""

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
from schemas.schemas import User
import os
from sqlalchemy import select
from services.logging_utils import log_to_redis_stream
from database.database import SessionLocal
from models.models import User as UserModel

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY env var must be set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    """
    Authenticate a user by username and password.

    Args:
        username (str): The username.
        password (str): The plain text password.

    Returns:
        UserModel or None: The user object if
        authentication succeeds, None otherwise.
    """

    async with SessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        log_to_redis_stream(f"Authentication failed for user: {username}")
        return None
    return user


async def create_user(username: str, password: str):
    """
    Create a new user with the given username and password.

    Args:
        username (str): The username.
        password (str): The plain text password.

    Returns:
        UserModel or None: The created user object,
        or None if user already exists.
    """

    async with SessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = result.scalar_one_or_none()
        if user:
            log_to_redis_stream(f"User already exists: {username}")
            return None
        hashed_password = pwd_context.hash(password)
        new_user = UserModel(
            username=username, hashed_password=hashed_password
        )
        session.add(new_user)
        await session.commit()
        log_to_redis_stream(f"User created successfully: {username}")
        return new_user


async def get_current_user(request: Request) -> User:
    """
    Retrieve the current user from the request using JWT token.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        UserModel: The user object.

    Raises:
        HTTPException: If token is missing or user not found.
    """

    token = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return RedirectResponse(url="/logout")
    except JWTError:
        return RedirectResponse(url="/logout")

    async with SessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(username=user.username, disabled=user.disabled)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The payload data.
        expires_delta (timedelta, optional): Expiration time for the token.

    Returns:
        str: The encoded JWT token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(token: str):
    """
    Verify a JWT token and return the associated user.

    Args:
        token (str): The JWT token.

    Returns:
        User or None: The user object if token is valid, None otherwise.
        RedirectResponse: If token is expired or invalid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None

        async with SessionLocal() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.username == username)
            )
            user = result.scalar_one_or_none()
            return user

        if user:
            return User(username=user.username, disabled=user.disabled)
        return None
    except jwt.ExpiredSignatureError:
        return RedirectResponse(url="/logout")
    except jwt.InvalidTokenError:
        return RedirectResponse(url="/logout")
