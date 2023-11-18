from fastapi import APIRouter, File, UploadFile


upload_router = APIRouter()


@upload_router.post("/uploadfile/")
async def upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}
