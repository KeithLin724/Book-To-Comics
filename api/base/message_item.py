from pydantic import BaseModel


class GenerateImageOldItem(BaseModel):
    name: str = "tmp"
    prompt: str


class GenerateImageItem(BaseModel):
    name: str = "tmp"
    prompt: str
    unique_id: str


class ChatItem(BaseModel):
    name: str = "tmp"
    model: str = "gpt-3.5-turbo"
    prompt: str


class ResultItems(BaseModel):
    unique_id: str
    file_path: str = None
    file_name: str = None
    time: str = None
    request_path: str = None


class ConnectPlugItem(BaseModel):
    type_name: str
    url: str
    check_alive_root: str
    method_root: str


class GenerateServiceItem(BaseModel):
    type_service: str = "chat"
    name: str = "tmp"
    prompt: str


class ResultServiceItems(BaseModel):
    type_service: str
    unique_id: str
    task_id: str = None
    file_path: str = None
    file_name: str = None
    time: str = None
    request_path: str = None
