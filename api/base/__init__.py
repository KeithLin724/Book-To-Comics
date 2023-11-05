import socket
from model import TextToImage, TextGenerator
import os
from rq import Queue
from redis import Redis
from func import api_json
import logging

REDIS_CONNECT = Redis(host="localhost", port=6379)
TASK_IMAGE_QUEUE = Queue("generate-image-queue", connection=REDIS_CONNECT)


def get_local_ip():
    try:
        # 创建一个临时的套接字连接到一个远程地址，然后获取本地 IP 地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 这里的远程地址可以是任意已知 IP 地址和端口
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return "127.0.0.1"


SERVER_IP = get_local_ip()
SERVER_PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

text_to_image_model = TextToImage()


text_generator_model = TextGenerator()

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")
G4F_VERSION = TextGenerator.G4F_VERSION

LOGGER = logging.getLogger("uvicorn")


def save_server_data_to_json():
    data = {"ip": SERVER_IP, "port": SERVER_PORT}
    api_json.json_to_file(data, "server_data.json")
    return


def handle_user_folder(user_name) -> str:
    """
    The function creates a folder for a user if it doesn't already exist and returns the path to the
    folder.

    :param user_name: The `user_name` parameter is a string that represents the name of the user
    :return: the path to the user's folder.
    """
    path = os.path.join(IMAGE_FOLDER_PATH, user_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


from .message_item import GenerateImageItem, ChatItem, ResultItems, ConnectPlugItem
from .server_schedule import MonitorMicroServer

monitor_micro_server = MonitorMicroServer()


async def server_init():
    save_server_data_to_json()
    text_to_image_model.load()
    monitor_micro_server.start()
    LOGGER.info(f"server is open , URL :{SERVER_URL}")
    return


async def server_close():
    monitor_micro_server.close(out=LOGGER.info)
    LOGGER.info(f"server is close")
    return
