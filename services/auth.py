from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from schemas.schemas import User, InternalUser
import os

SECRET_KEY = os.getenv("SECRET_KEY", "asecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_user_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": pwd_context.hash("testpassword"),
        "disabled": False,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user_dict = fake_user_db.get(username)
    if not user_dict or not verify_password(password, user_dict['hashed_password']):
        return None

    return InternalUser(**user_dict)

def get_current_user(request: Request) -> User:
    token = None

    # Try to get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    # Fallback to cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = fake_user_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return User(username=user["username"], disabled=user["disabled"])

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        user_data = fake_user_db.get(username)
        return User(**user_data) if user_data else None
    except jwt.ExpiredSignatureError:
        return None
        # raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        return None
        # raise HTTPException(status_code=401, detail="Invalid token")
    

# @router.post("/login")
# async def access_token_login(form_data: OAuth2PasswordRequestForm = Depends()):
#     if form_data.username != fake_user['username'] or not pwd_context.verify(form_data.password, fake_user['hashed_password']):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(
#         data={"sub": form_data.username},
#         expires_delta=timedelta(minutes=5)
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
