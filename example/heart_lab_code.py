from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import requests

app = FastAPI()

LAB_SERVER_URL = "http://lab_server_ip:lab_server_port"  # 用实际的Lab服务器URL替换


def send_heartbeat():
    try:
        response = requests.get(f"{LAB_SERVER_URL}/heartbeat")
        if response.status_code == 200:
            print("已发送心跳到Lab服务器。")
        else:
            print("无法发送心跳到Lab服务器。")
    except requests.exceptions.RequestException:
        print("Lab服务器无法访问。")


scheduler = BackgroundScheduler()
scheduler.add_job(send_heartbeat, "interval", seconds=5)  # 每5秒发送一次心跳
scheduler.start()


@atexit.register
def close_scheduler():
    scheduler.shutdown()


@app.get("/")
async def read_root():
    return {"message": "Home FastAPI服务器正在运行"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
