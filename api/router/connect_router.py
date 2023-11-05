from fastapi import APIRouter
from base import monitor_micro_server

connect_api_router = APIRouter()


@connect_api_router.post("/connect")
async def connect_plug():
    return {"message": "not ready"}


@connect_api_router.get("/connect")
async def display_micro_service():
    return monitor_micro_server.get_all_micro_service()
