import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR


async def job_function():
    print("Job executed successfully")


def on_job_executed(event):
    print(f"Job ID: {event.job_id} executed successfully")


def on_job_error(event):
    print(f"Job ID: {event.job_id} encountered an error: {event.exception}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_listener(on_job_executed, EVENT_JOB_EXECUTED)
    scheduler.add_listener(on_job_error, EVENT_JOB_ERROR)
    scheduler.start()

    # 添加一个作业，每隔5秒执行一次
    job = scheduler.add_job(job_function, "interval", seconds=1)

    # 在10秒后删除作业
    await asyncio.sleep(10)
    scheduler.remove_job(job.id)
    scheduler.print_jobs()

    await asyncio.sleep(10)
    scheduler.shutdown()
    scheduler.print_jobs()


if __name__ == "__main__":
    asyncio.run(main())
