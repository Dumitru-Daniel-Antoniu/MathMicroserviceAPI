from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest
from contextlib import asynccontextmanager
from controllers.controllers import router as math_router
from database.database import get_db
from services.cache import init_cache

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

app.include_router(math_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/statistics", response_class=HTMLResponse)
async def statistics(request: Request):
    statistics = generate_latest().decode()

    return templates.TemplateResponse(
        "statistics.html",
        {
            "request": request,
            "statistics": statistics
        }
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
