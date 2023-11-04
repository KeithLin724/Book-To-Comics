from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()

connected_clients = set()


def my_background_task():
    for client in connected_clients:
        client.send_text("This is a message from the server")


@app.on_event("startup")
def startup_event():
    trigger = IntervalTrigger(seconds=5)
    scheduler.add_job(my_background_task, trigger)


@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
