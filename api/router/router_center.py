from fastapi import APIRouter


from .chat_router import chat_router
from .text_to_image_router import text_to_image_router
from .connect_router import connect_api_router
from .upload_router import upload_router

router_center = APIRouter()
router_center.include_router(router=chat_router)
router_center.include_router(router=text_to_image_router)
router_center.include_router(router=connect_api_router)
router_center.include_router(router=upload_router)
