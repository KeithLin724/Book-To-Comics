from pydantic import BaseModel


class GenerateImageItem(BaseModel):
    name: str = "tmp"
    prompt: str
    unique_id: str


class ResultItems(BaseModel):
    unique_id: str
    file_path: str = None
    file_name: str = None
    time: str = None
    request_path: str = None
