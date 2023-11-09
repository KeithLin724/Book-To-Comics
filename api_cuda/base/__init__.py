import os
import socket
from . import api_func, api_json

# import api_json
from model import TextToImage
import logging
from redis import Redis

from .client_scheduler import MonitorServer

LAB_SERVER_IP, LAB_SERVER_PORT = "140.113.238.35", 5000

REDIS_CONNECT = Redis(host=LAB_SERVER_IP, port=6379)

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 4080

SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")
LOGGER = logging.getLogger("uvicorn")

text_to_image_model = TextToImage()

SERVER_TYPE = {
    "type_name": "text_to_image",
    "url": SERVER_URL,
    "check_alive_root": "is_live",
    "method_root": "generate_redis",
}

monitor_server = MonitorServer(
    connect_server_url=f"http://{LAB_SERVER_IP}:{LAB_SERVER_PORT}/connect",
    send_to_server_json=SERVER_TYPE,
)


def save_server_data_to_json():
    data = {
        "ip": SERVER_IP,
        "port": SERVER_PORT,
        "url": SERVER_URL,
    }
    api_json.json_to_file(data, "server_data(text_to_image).json")
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


async def server_init():
    save_server_data_to_json()
    text_to_image_model.load()
    monitor_server.start()

    if not os.path.exists(IMAGE_FOLDER_PATH):
        os.makedirs(IMAGE_FOLDER_PATH)

    LOGGER.info(f"server is open, URL : {SERVER_URL}")
    return


async def server_close():
    monitor_server.close()
    LOGGER.info(f"server is close")
    return


from .message_item import GenerateImageItem, ResultItems
