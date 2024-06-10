from fastapi import FastAPI
from src.api.healthcheck import router as health_router
from src.api import api_router

app = FastAPI()

app.include_router(health_router)
app.include_router(api_router)
