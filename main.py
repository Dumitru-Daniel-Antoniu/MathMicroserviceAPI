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
async def statistics():
    statistics = generate_latest().decode()

    return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
          <head>
            <title>Application Metrics</title>
            <link rel="icon" href="/static/statistics.png" type="image/x-icon">
            <style>
              body {{
                font-family: 'Courier New', monospace;
                background-color: #1e1e1e;
                color: #dcdcdc;
                padding: 2rem;
                margin: 0;
              }}
              h1 {{
                color: #00d8ff;
              }}
              pre {{
                background-color: #2e2e2e;
                padding: 1rem;
                border-radius: 5px;
                overflow-x: auto;
                white-space: pre-wrap;
              }}
              .panel {{
                background-color: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
              }}
              .panel h2 {{
                font-size: 1.3rem;
                color: #333;
                margin-bottom: 1rem;
              }}
              iframe {{
                border: none;
                width: 100%;
                height: 300px;
                border-radius: 4px;
              }}
            </style>
          </head>
          <body>
            <h1>Application Metrics</h1>
            
            <div class="panel">
              <h2>📊 Cache Hits Total</h2>
              <iframe src="http://localhost:3000/d-solo/6fccc10e-eb7b-4d39-992f-b3c1218c4ae5/cache-hits-total?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>📉 Cache Misses Total</h2>
              <iframe src="http://localhost:3000/d-solo/f1b123db-d23c-45b3-90fe-de9395cbd517/cache-misses-total?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>⏱️ HTTP Request Duration (Seconds)</h2>
              <iframe src="http://localhost:3000/d-solo/c8a18fb3-e2e4-446c-b663-b8620ee31466/http-request-duration-seconds?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>📏 HTTP Request Duration High resolution (Seconds)</h2>
              <iframe src="http://localhost:3000/d-solo/d995f02e-18b3-454b-89d5-b1f863d374d9/http-request-duration-highr-seconds?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>📬 HTTP Requests Total</h2>
              <iframe src="http://localhost:3000/d-solo/8ab65fa9-10bd-4cb8-b884-67c5dd6e761a/http-requests-total?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>📦 HTTP Request Size (Bytes)</h2>
              <iframe src="http://localhost:3000/d-solo/8945855c-1b02-4561-b72f-525b0f6a951c/http-request-size-bytes?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
        
            <div class="panel">
              <h2>📤 HTTP Response Size (Bytes)</h2>
              <iframe src="http://localhost:3000/d-solo/7ad572e4-e845-449e-9d9c-817e888b7595/http-response-size-bytes?orgId=1&refresh=5s&from=now-15m&to=now&timezone=browser&panelId=1&__feature.dashboardSceneSolo=true" width="450" height="200" frameborder="0"></iframe>
            </div>
            
            <pre>{statistics}</pre>
          </body>
        </html>
    """)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

Instrumentator().instrument(app).expose(app, endpoint="/metrics")
