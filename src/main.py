from fastapi import FastAPI
from .api.healthcheck import router as health_router
from .api import api_router as api_v1_router

app = FastAPI()


app.include_router(health_router)
app.include_router(api_v1_router)
