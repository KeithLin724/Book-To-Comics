from rq import Worker, Queue, Connection
from redis import Redis


# 连接到Redis队列
redis_conn = Redis(host="localhost", port=6379)
with Connection(redis_conn):
    q = Queue("generate-image-queue")
    worker = Worker([q])
    worker.work()
