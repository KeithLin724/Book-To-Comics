from fastapi import APIRouter
from base import monitor_micro_server, ConnectPlugItem

connect_api_router = APIRouter()


@connect_api_router.post("/connect")
async def connect_plug(connect_plug_item: ConnectPlugItem):
    monitor_micro_server.add_micro_server(
        micro_server_name=connect_plug_item.type_name,
        micro_server_url=connect_plug_item.url,
    )
    return {"message": "OK"}


@connect_api_router.get("/connect")
async def display_micro_service():
    return monitor_micro_server.get_all_micro_service()
