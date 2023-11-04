from fastapi import APIRouter


connect_api_router = APIRouter()


@connect_api_router.post("/connect")
async def connect_plug():
    return
