from pydantic import BaseModel


class GenerateImageItem(BaseModel):
    name: str = "tmp"
    prompt: str


class ChatItem(BaseModel):
    model: str = "gpt-3.5-turbo"
    message: str


class ResultItems(BaseModel):
    unique_id: str
    file_path: str = None
    file_name: str = None
    time: str = None
    request_path: str = None


class ConnectPlugItem(BaseModel):
    type_name: str
    url: str
