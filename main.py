from http.client import HTTPException

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest
from contextlib import asynccontextmanager

from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from controllers.controllers import router
from database.database import get_db
from services.cache import init_cache
from services.auth import verify_token, get_current_user
from schemas.schemas import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db()
    await init_cache()
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )

    return app

app = create_app()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/statistics", tags=["Metrics"])
async def statistics(request: Request):
    try:
        user = await get_current_user(request)
    except Exception as e:
        if "text/html" in request.headers.get("accept", ""):
            return RedirectResponse(url="/")
        raise e

    statistics = generate_latest().decode()
    return templates.TemplateResponse(
        "statistics.html",
        {
            "request": request,
            "statistics": statistics
        }
    )

@app.get("/", tags=["Application"])
async def root(request: Request):
    token = request.cookies.get("access_token")
    user = None
    if token:
        user = await verify_token(token)
    if user:
        return templates.TemplateResponse("menu.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("login.html", {"request": request})

Instrumentator().instrument(app).expose(app)
