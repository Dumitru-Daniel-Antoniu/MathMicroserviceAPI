from fastapi import FastAPI
from database import get_db
from controllers import router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await get_db()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
