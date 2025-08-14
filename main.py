"""
Main FastAPI application entry point.

Initializes the FastAPI app with database and cache setup,
mounts static files, configures Jinja2 templates, and exposes Prometheus
metrics. Includes routes for application root and statistics, handling
user authentication and rendering templates.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest
from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse
from controllers.controllers import router
from database.database import get_db
from services.cache import init_cache
from services.auth import verify_token, get_current_user
from models.models import User as UserModel
from database.database import get_request


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.

    Initializes the database and cache before the app starts.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    await get_db()
    await init_cache()
    yield


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """

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
    """
    Display application statistics and Prometheus metrics.

    Authenticates the user, fetches metrics
    and renders the statistics template.
    Redirects to root if authentication fails.

    Args:
        request (Request): Incoming HTTP request.

    Returns:
        TemplateResponse or RedirectResponse:
            Rendered statistics page or redirect.
    """

    try:
        user = await get_current_user(request)
        print("User connected: ")
        print(user.username)
    except Exception as e:
        if "text/html" in request.headers.get("accept", ""):
            return RedirectResponse(url="/")
        raise e

    statistics = generate_latest().decode()
    await get_request("/statistics")
    return templates.TemplateResponse(
        "statistics.html",
        {
            "request": request,
            "statistics": statistics
        }
    )


@app.get("/", tags=["Application"])
async def root(request: Request):
    """
    Render the application root page.

    Checks for user authentication via access token and renders
    either the menu or login template accordingly.

    Args:
        request (Request): Incoming HTTP request.

    Returns:
        TemplateResponse: Rendered menu or login page.
    """

    token = request.cookies.get("access_token")
    user = None
    if token:
        user = await verify_token(token)
    if user and type(user) is UserModel:
        return templates.TemplateResponse("menu.html",
                                          {"request": request, "user": user})
    else:
        return templates.TemplateResponse("login.html", {"request": request})


Instrumentator().instrument(app).expose(app)
