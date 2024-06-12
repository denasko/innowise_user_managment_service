from fastapi import FastAPI
from src.api import api_router
from src.api.healthcheck import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(api_router)
