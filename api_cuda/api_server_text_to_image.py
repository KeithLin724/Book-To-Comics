from fastapi import FastAPI
from base import SERVER_IP, SERVER_PORT, SERVER_URL, server_init, server_close

from router import text_to_image_router, receiver_router
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    "open server do"
    await server_init()
    yield
    "close server"
    await server_close()
    return


app = FastAPI(title="Text to image server", lifespan=lifespan)
app.include_router(router=text_to_image_router)
app.include_router(router=receiver_router)


@app.get("/")
async def home():
    return {
        "message": "hello, welcome to Text to image",
        "ip": SERVER_IP,
        "port": SERVER_PORT,
        "url": SERVER_URL,
    }


if __name__ == "__main__":
    uvicorn.run(host=SERVER_IP, port=SERVER_PORT)
