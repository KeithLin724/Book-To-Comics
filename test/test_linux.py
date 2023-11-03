from redis import Redis
from rq import Queue, Worker

qfail = Queue("generate-image-queue", connection=Redis(host="localhost", port=6379))

new = Worker([qfail], connection=Redis(host="localhost", port=6379), name="work2")
print(qfail.count)

new.work()
