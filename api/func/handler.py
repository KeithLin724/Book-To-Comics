from fastapi.responses import StreamingResponse, JSONResponse, Response

import io
import json
import httpx

from base import (
    monitor_micro_server,
    ResultServiceItems,
    TASK_IMAGE_QUEUE,
    REDIS_CONNECT,
)


async def handle_request_result_function(result_service: ResultServiceItems):
    """The function `handle_request_result_function` handles the result of a service request.

    Parameters
    ----------
    result_service : ResultServiceItems
        The parameter `result_service` is an instance of the `ResultServiceItems` class. It is used to pass
    information about the result of a service request. The `ResultServiceItems` class likely has
    attributes such as `type_service` which stores the type of service requested (e.g., "

    Returns
    -------
        a response.

    """
    type_of_service = result_service.type_service

    if type_of_service == "text_to_image":
        response = await handle_text_to_image_result(result_service=result_service)
        return response

    return


async def handle_text_to_image_result(result_service: ResultServiceItems) -> Response:
    unique_id, task_id = result_service.unique_id, result_service.task_id

    # TODO: check is in queue or finish

    if task_id is not None:
        job = TASK_IMAGE_QUEUE.fetch_job(task_id)

        if not job.is_finished:
            return JSONResponse(
                content={
                    "job_state": job.get_status(),
                    "message": f"task id:{task_id}, state is {job.get_status()}",
                }
            )

    # * is finish

    # TODO: get from redis
    # find the redis server is have it
    if unique_id and (image_in_server := REDIS_CONNECT.get(unique_id)) is not None:
        image_in_server = io.BytesIO(image_in_server)
        response = StreamingResponse(image_in_server, media_type="image/jpeg")

        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{unique_id}.jpg"'

        return response

    # TODO: get result from micro service
    json_data = {
        "unique_id": result_service.unique_id,
        "file_path": result_service.file_path,
    }

    micro_service_url = monitor_micro_server.get_micro_service_url(
        micro_service_name=result_service.type_service,
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
