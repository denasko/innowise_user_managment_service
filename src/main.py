from fastapi import FastAPI
from src.api import api_router
from src.api.healthcheck import router as health_router
from src.core.middleware import BearerMiddleware

app = FastAPI()

app.include_router(health_router)
app.include_router(api_router)
app.add_middleware(BearerMiddleware)
