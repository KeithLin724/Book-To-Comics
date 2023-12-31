from fastapi import APIRouter
from fastapi.responses import FileResponse, StreamingResponse
import uuid
import datetime
import os
import io


from base import (
    SERVER_IP,
    SERVER_PORT,
    text_to_image_model,
    REDIS_CONNECT,
    IMAGE_FOLDER_PATH,
    message_item,
)

from func import api_func

text_to_image_router = APIRouter()


@text_to_image_router.post("/generate-redis")
async def generate_image(generate_image_json: message_item.GenerateImageItem):
    """
    The `generate_image` function takes a user's name and prompt, generates an image based on the
    prompt, saves the image to a file, and returns information about the generated image.

    :param generate_image_json: The parameter `generate_image_json` is of type `GenerateImageItem`. It
    is an object that contains the following attributes:
    :type generate_image_json: GenerateImageItem
    :return: a dictionary with the following keys and values:
    - "id": unique_file_name (a unique identifier for the generated image)
    - "file_path": file_path (the path where the image file is saved)
    - "file_name": file_name (the name of the image file)
    - "time": now_time (the current timestamp)
    - "request-path": f"http://{
    """
    user_name, user_prompt = generate_image_json.name, generate_image_json.prompt

    image = await text_to_image_model.generate_with_async(user_prompt)

    now_time = datetime.datetime.now()

    # make a unique file name
    # unique_file_name = uuid.uuid5(
    #     namespace=uuid.NAMESPACE_DNS,
    #     name=f"{user_name}_{user_prompt}_{now_time}",
    # )
    unique_file_name = generate_image_json.unique_id

    file_path, file_name = (
        IMAGE_FOLDER_PATH,
        f"{unique_file_name}.jpg",
    )

    file_path = os.path.join(file_path, file_name)

    image.save(file_path)
    id_key = str(unique_file_name)
    image_bytes = api_func.image_to_bytes(image)

    REDIS_CONNECT.set(id_key, image_bytes)

    REDIS_CONNECT.expire(id_key, 86400)  # save in server 1 days

    return {
        "unique_id": unique_file_name,
        "file_path": file_path,
        "file_name": file_name,
        "time": now_time,
        "request-path": f"http://{SERVER_IP}:{SERVER_PORT}/result",
    }


@text_to_image_router.post("/result")
async def replay_image(requestItem: message_item.ResultItems):
    """
    The `replay_image` function takes a `requestItem` object containing a unique ID and file path, and
    returns a response with the corresponding image file if it exists, either from the file system or a
    Redis server.

    :param requestItem: The `requestItem` parameter is an object of type `ResultItems`. It contains two
    attributes:
    :type requestItem: ResultItems
    :return: The function `replay_image` returns a response object. The type of response object returned
    depends on the conditions met in the code.
    """
    unique_id, file_path = requestItem.unique_id, requestItem.file_path

    # check the file path
    if file_path is not None and os.path.exists(file_path):
        response = FileResponse(file_path, media_type="image/jpeg")

        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{unique_id}.jpg"'

        return response

    # find the redis server is have it
    if unique_id and (image_in_server := REDIS_CONNECT.get(unique_id)) is not None:
        image_in_server = io.BytesIO(image_in_server)
        response = StreamingResponse(image_in_server, media_type="image/jpeg")

        response.headers[
            "Content-Disposition"
        ] = f'attachment; filename="{unique_id}.jpg"'

        return response

    # make the file path and check it
    file_path = os.path.join(IMAGE_FOLDER_PATH, f"{unique_id}.png")
    if not os.path.exists(file_path):
        return {"error": "can not find the file about this id"}

    response = FileResponse(file_path, media_type="image/jpeg")

    response.headers["Content-Disposition"] = f'attachment; filename="{unique_id}.jpg"'

    return response
