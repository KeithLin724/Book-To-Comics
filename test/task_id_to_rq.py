import redis
from rq.job import Job
import asyncio
import time
import json

redis_conn = redis.Redis(host="140.113.238.35", port=6379)


async def get_job_result(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)

    def wait_job():
        while not job.is_finished:
            # 获取任务的执行结果
            time.sleep(1)
        result = job.result  # 这将阻塞，直到任务完成
        return result

    return await asyncio.to_thread(wait_job)


async def main():
    # 连接到Redis服务器

    job_id = input("id:")
    # 创建RQ队列
    # queue = Queue(connection=redis_conn)
    result = await get_job_result(job_id=job_id)
    # 输出任务的结果
    result = json.loads(result.content)
    print("Task result:", result)
    return


asyncio.run(main())
