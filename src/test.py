# worker.py

import os
from rq import Queue, get_current_job
from redis import Redis, StrictRedis
import time
from test_math import calculate_factorial

# Connect to the Redis server
# redis_connection = Redis(host="localhost", port=6379, db=0)
# print(redis_connection)
# Create an RQ queue
queue = Queue("test_worker", connection=StrictRedis())


# Define a function to calculate the factorial of a number


if __name__ == "__main__":
    # Enqueue a task to calculate the factorial of 10
    job = queue.enqueue(calculate_factorial, 10)

    print(f"Task ID: {job.get_id()}")

    # Wait for the task to complete and print the result
    while not job.is_finished:
        time.sleep(1)

    result = job.result
    print(f"Factorial of 10 is: {result}")
