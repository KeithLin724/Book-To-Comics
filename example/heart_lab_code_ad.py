from fastapi import FastAPI, Depends
from fastapi.routing import Request, Depends, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi import FastAPI, Depends
from fastapi.routing import Request, Depends, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()


def my_background_task():
    print("This is a background task that runs every 5 seconds")


@app.on_event("startup")
def startup_event():
    trigger = IntervalTrigger(seconds=5)
    scheduler.add_job(my_background_task, trigger)


@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down the FastAPI application")
    scheduler.shutdown()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
