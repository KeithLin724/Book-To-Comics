from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, StreamingResponse
import json
import httpx
import io


# import uvicorn
import router
from base import (
    SERVER_IP,
    SERVER_PORT,
    SERVER_URL,
    # redis queue
    TASK_IMAGE_QUEUE,
    # Item
    ChatItem,
    GenerateServiceItem,
    ResultServiceItems,
    GenerateImageOldItem,
    G4F_VERSION,
    LOGGER,
    # server lifespan
    server_init,
    server_close,
    monitor_micro_server,
    chat_to_ai_fast_function,
)
from api_task_func import generate_image_queue
from worker_listener import WorkListener
from contextlib import asynccontextmanager

# from func import helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """The `lifespan` function is an asynchronous generator that initializes and closes a server for a
    FastAPI application.

    Parameters
    ----------
    app : FastAPI
        The `app` parameter is of type `FastAPI`. It represents the FastAPI application instance that is
    being passed to the `lifespan` function.

    Returns
    -------
        a generator object.

    """
    # open server do
    # worker_listener = WorkListener([TASK_IMAGE_QUEUE])
    # worker_listener.start()
    await server_init()
    # await start_listener_worker()
    yield
    # close server
    # worker_listener.close()
    await server_close()
    return


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

app.include_router(router=router.test_router)
app.include_router(router=router.router_center)


@app.get("/")
async def home(request: Request):
    LOGGER.info(SERVER_URL)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "g4f_version": G4F_VERSION,
            "url_link": SERVER_URL,
        },
    )


@app.post("/generate_service")
async def generate_request_to_micro_service(generate_service: GenerateServiceItem):
    """The function `generate_request_to_micro_service` generates a request to a microservice based on the
    provided `GenerateServiceItem` object.

    Parameters
    ----------
    generate_service : GenerateServiceItem
        The `generate_service` parameter is an instance of the `GenerateServiceItem` class. It contains the
    following attributes:

    Returns
    -------
        The function `generate_request_to_micro_service` returns different values depending on the
    conditions:

    """
    json_data = {
        "name": generate_service.name,
        "prompt": generate_service.prompt,
    }

    if generate_service.type_service == "chat":
        provider, result = await chat_to_ai_fast_function(
            prompt=generate_service.prompt
        )

        return {
            "provider": provider,
            "message": result,
        }

    if generate_service.type_service in monitor_micro_server:
        response = await handle_request_function(generate_service, json_data)
        return response

    return {"error": f"This service({generate_service.type_service}) is not available"}


async def handle_request_function(
    generate_service: GenerateServiceItem,
    json_data: dict,
):
    """The function `handle_request_function` handles a specific type of service called "text_to_image" by
    enqueueing a job to a task queue and returning the task ID.

    Parameters
    ----------
    generate_service : GenerateServiceItem
        GenerateServiceItem is a class that represents a service to be generated. It has a property called
    "type_service" which indicates the type of service to be generated.
    json_data : dict
        The `json_data` parameter is a dictionary that contains the data needed for the function to
    generate the desired service. The specific contents of the `json_data` dictionary would depend on
    the requirements of the `generate_service` and `generate_image_queue` functions.

    Returns
    -------
        a dictionary with a key "task_id" and the value being the ID of the job that was enqueued.

    """
    if generate_service.type_service == "text_to_image":
        micro_service_method_url = monitor_micro_server.get_micro_service_method_url(
            micro_service_name=generate_service.type_service,
        )

        unique_id = helper.to_unique_id(
            user_name=generate_service.name,
            user_prompt=generate_service.prompt,
        )

        json_data |= {"unique_id": unique_id}

        job = TASK_IMAGE_QUEUE.enqueue(
            generate_image_queue,
            micro_service_method_url,
            json_data,
            timeout=7200,
        )
        return {
            "task_id": job.get_id(),
            "unique_id": unique_id,
        }

    return


@app.post("/result_service")
async def request_to_micro_service_get_result(result_service_item: ResultServiceItems):
    # type_of_service = result_service_item.type_service

    if result_service_item.type_service in monitor_micro_server:
        response = await handle_request_result_function(
            result_service=result_service_item
        )
        return response

    return {"error": f"service ({result_service_item.type_service}) is close"}


async def handle_request_result_function(result_service: ResultServiceItems):
    type_of_service = result_service.type_service

    if type_of_service == "text_to_image":
        json_data = {
            "unique_id": result_service.unique_id,
            "file_path": result_service.file_path,
        }

        micro_service_url = monitor_micro_server.get_micro_service_url(
            micro_service_name=type_of_service,
        )

        # get the result from the micro service
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{micro_service_url}/result", json=json_data)

        content_type = response.headers.get("Content-Type")

        # handle the content type
        if content_type == "image/jpeg":
            image_bytes = io.BytesIO(response.content)
            return_response = StreamingResponse(image_bytes, media_type="image/jpeg")
            response.headers["Content-Disposition"] = response.headers.get(
                "Content-Disposition", ""
            )

            return return_response

        # error message
        return JSONResponse(content=json.loads(response.content))

    return


@app.post("/generate")
async def generate_image_request(generate_image_json: GenerateImageOldItem):
    """
    The function `generate_image_request` enqueues a job to a Redis queue with the specified parameters
    and returns the task ID.

    :param generate_image_json: The parameter `generate_image_json` is of type `GenerateImageItem`
    :type generate_image_json: GenerateImageItem
    :return: a dictionary with a single key-value pair. The key is "task_id" and the value is the ID of
    the job that was enqueued in the TASK_IMAGE_QUEUE.
    """
    unique_id = helper.to_unique_id(
        user_name=generate_image_json.name,
        user_prompt=generate_image_json.prompt,
    )

    job = TASK_IMAGE_QUEUE.enqueue(
        generate_image_queue,
        f"http://{SERVER_IP}:{SERVER_PORT}/generate-redis",
        {
            "name": generate_image_json.name,
            "prompt": generate_image_json.prompt,
            "unique_id": unique_id,
        },
    )
    return {"task_id": job.get_id()}


# https://blog.csdn.net/qq_33801641/article/details/120320780
# if __name__ == "__main__":
#     init_app()
# uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
