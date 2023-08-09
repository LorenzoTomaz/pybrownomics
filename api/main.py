from typing import Union
from motor import motor_asyncio

from fastapi import FastAPI
from server.routes.simulation import router as SimulationRouter

app = FastAPI()


app.include_router(SimulationRouter, tags=["Simulation"], prefix="/simulation")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


