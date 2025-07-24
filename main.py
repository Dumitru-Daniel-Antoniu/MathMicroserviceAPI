from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from controllers.controllers import router as math_router
from database.database import get_db
from services.cache import init_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db()
    await init_cache()
    yield

app = FastAPI(title="Math Microservice API",
              version="1.0.0",
              lifespan=lifespan)

app.include_router(math_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
