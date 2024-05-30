from typing import Union
from src.routers.test_docker_routers import docker_router
from fastapi import FastAPI

from src.routers.healthcheck import router as health_router

app = FastAPI()
app.include_router(health_router)
app.include_router(docker_router, prefix="/api/v1")


@app.post("/auth/signup")
def signup():
    return {"Hello": "World"}


