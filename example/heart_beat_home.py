from fastapi import FastAPI
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = FastAPI()

last_heartbeat_time = None


def check_heartbeat():
    global last_heartbeat_time
    if last_heartbeat_time is not None:
        time_difference = datetime.now() - last_heartbeat_time
        if time_difference.total_seconds() > 10:  # 调整需要的阈值
            print("Home服务器未发送心跳。")


scheduler = BackgroundScheduler()
scheduler.add_job(check_heartbeat, "interval", seconds=5)  # 每5秒检查一次心跳
scheduler.start()


@atexit.register
def close_scheduler():
    scheduler.shutdown()


@app.get("/")
async def read_root():
    return {"message": "Lab FastAPI服务器正在运行"}


@app.get("/heartbeat")
async def send_heartbeat():
    global last_heartbeat_time
    last_heartbeat_time = datetime.now()
    return {"message": "Lab服务器已收到心跳"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
