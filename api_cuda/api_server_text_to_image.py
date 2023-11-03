from fastapi import FastAPI
from base import (
    SERVER_IP,
    SERVER_PORT,
    SERVER_URL,
)
from router import text_to_image_router

app = FastAPI()
app.include_router(router=text_to_image_router)


@app.get("/")
async def home():
    return {
        "message": "hello, welcome to Text to image",
        "ip": SERVER_IP,
        "port": SERVER_PORT,
        "url": SERVER_URL,
    }
