from fastapi import APIRouter
from fastapi.responses import FileResponse

test_router = APIRouter()


@test_router.get("/test")
async def test():
    # from base import FOLDER_PATH

    return {"result": "ready"}


@test_router.get("/test_result")
async def test_result():
    return {"result": "not ready"}


@test_router.post("/test_result")
async def test_result_post():
    return {"result": "not ready"}


@test_router.get("/test_get_prompt")
async def test_get_prompt():
    return {
        "prompt": [
            "cat is running",
            "i am iron man",
            "dog is running",
        ],
    }


@test_router.get("/test_get_image")
async def test_get_image():
    test_image_path, test_image_name = "./images/cat.jpg", "cat"

    response = FileResponse(
        test_image_path,
        media_type="image/jpeg",
    )

    # response.headers[
    #     "Content-Disposition"
    # ] = f'attachment; filename="{test_image_name}.jpg"'

    return response
