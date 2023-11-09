from fastapi import APIRouter
from base import monitor_server

# `receiver_router = APIRouter()` is creating an instance of the `APIRouter` class from the FastAPI
# framework. This instance can be used to define routes and endpoints for the server.
receiver_router = APIRouter()


@receiver_router.get("/is_live")
async def is_live_check():
    monitor_server.server_check_point(server_check=True)
    return {"message": "OK"}
