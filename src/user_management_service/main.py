from typing import Union

from fastapi import FastAPI

from src.routers.healthcheck import router as health_router

app = FastAPI()
app.include_router(health_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
