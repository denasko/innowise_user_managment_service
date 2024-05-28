from typing import Union

from fastapi import FastAPI

from src.routers.healthcheck import router as health_router

app = FastAPI()
app.include_router(health_router)


@app.post("/auth/signup")
def signup():
    return {"Hello": "World"}


@app.post("/auth/login")
def login(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
