from rq import Worker, Queue, Connection
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
print(SERVER_IP)
# 连接到Redis队列
redis_conn = Redis(host=SERVER_IP, port=6379)
with Connection(redis_conn):
    q = Queue("generate-image-queue")
    worker = Worker([q])
    worker.work()
