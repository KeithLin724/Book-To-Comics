import socket
from model import TextToImage, TextGenerator
import os
from rq import Queue
from redis import Redis
from func import api_json
import logging
from func import helper

REDIS_CONNECT = Redis(host="localhost", port=6379)
TASK_IMAGE_QUEUE = Queue("generate-image-queue", connection=REDIS_CONNECT)


SERVER_IP = helper.get_local_ip()
SERVER_PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

text_to_image_model = TextToImage()


text_generator_model = TextGenerator()

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")
G4F_VERSION = TextGenerator.G4F_VERSION

LOGGER = logging.getLogger("uvicorn")


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


async def chat_to_ai_fast_function(prompt: str):
    provider, reply_message = await text_generator_model.generate(prompt=prompt)
    return provider, reply_message


from .message_item import (
    GenerateImageItem,
    ChatItem,
    ResultItems,
    ConnectPlugItem,
    GenerateServiceItem,
    ResultServiceItems,
    GenerateImageOldItem,
)
from .server_schedule import MonitorMicroServer

monitor_micro_server = MonitorMicroServer()


async def server_init():
    helper.save_server_data_to_json(server_ip=SERVER_IP, server_port=SERVER_PORT)
    # text_to_image_model.load()
    monitor_micro_server.start()
    LOGGER.info(f"server is open , URL :{SERVER_URL}")
    return


async def server_close():
    monitor_micro_server.close(out=LOGGER.info)
    LOGGER.info(f"server is close")
    return
