from fastapi import FastAPI
import socket

app = FastAPI()
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000


@app.get("/")
async def home():
    return "Hello"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
