from rq import Worker, Queue, Connection
from redis import Redis
import os
from dotenv import load_dotenv
import api_task_func


load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
print(SERVER_IP)
# 连接到Redis队列
redis_conn = Redis(host=SERVER_IP, port=6379)
with Connection(redis_conn):
    q = Queue(
        "generate-image-queue",
        default_timeout=3600,
    )
    worker = Worker([q])
    worker.work()
