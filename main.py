import logging
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from controllers.controllers import router
from database.database import get_db
from services.cache import init_cache
from services.auth import verify_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db()
    await init_cache()
    yield

# logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Math Microservice API",
              version="1.0.0",
              lifespan=lifespan)

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    token = request.cookies.get("access_token")
    print(f"Token from cookies: {token}")
    user = None
    if token:
        user = verify_token(token)
        print(f"User from token: {user}")
    if user:
        return templates.TemplateResponse("index.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("login.html", {"request": request})
