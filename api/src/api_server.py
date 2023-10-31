from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import router
from base import (
    SERVER_IP,
    SERVER_PORT,
    TASK_IMAGE_QUEUE,
    GenerateImageItem,
    G4F_VERSION,
)
from api_task_func import generate_image_queue


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def init_app():
    app.include_router(router=router.test_router)
    app.include_router(router=router.ai_router)

    return


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "g4f_version": G4F_VERSION}
    )


@app.post("/generate")
async def generate_image_request(generate_image_json: GenerateImageItem):
    """
    The function `generate_image_request` enqueues a job to a Redis queue with the specified parameters
    and returns the task ID.

    :param generate_image_json: The parameter `generate_image_json` is of type `GenerateImageItem`
    :type generate_image_json: GenerateImageItem
    :return: a dictionary with a single key-value pair. The key is "task_id" and the value is the ID of
    the job that was enqueued in the TASK_IMAGE_QUEUE.
    """
    job = TASK_IMAGE_QUEUE.enqueue(
        generate_image_queue,
        f"http://{SERVER_IP}:{SERVER_PORT}/generate-redis",
        {
            "name": generate_image_json.name,
            "prompt": generate_image_json.prompt,
        },
    )
    return {"task_id": job.get_id()}


# https://blog.csdn.net/qq_33801641/article/details/120320780
if __name__ == "__main__":
    init_app()
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
