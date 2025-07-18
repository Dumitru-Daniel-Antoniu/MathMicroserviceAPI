from fastapi import FastAPI
from controllers import router as math_router

app = FastAPI(title="Math Microservice API", version="1.0.0")

app.include_router(math_router, prefix="/api/math", tags=["math operations"])

@app.get("/")
def root():
    return {"message": "Welcome to the Math Microservice API"}
