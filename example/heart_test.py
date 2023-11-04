from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from contextlib import asynccontextmanager


scheduler = BackgroundScheduler()
scheduler.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # trigger = IntervalTrigger(seconds=5)
    # scheduler.add_job(my_background_task, trigger)
    print("open server")
    yield

    # print("Shutting down the FastAPI application")
    # scheduler.shutdown()
    print("close server")
    return


app = FastAPI(lifespan=lifespan)


def my_background_task():
    print("This is a background task that runs every 5 seconds")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
