import socket
from model import TextToImage, TextGenerator
import os
from rq import Queue
from redis import Redis
from func import api_json
import logging

REDIS_CONNECT = Redis(host="localhost", port=6379)
TASK_IMAGE_QUEUE = Queue("generate-image-queue", connection=REDIS_CONNECT)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

text_to_image_model = TextToImage()
text_to_image_model.load()

text_generator_model = TextGenerator()

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")
G4F_VERSION = TextGenerator.G4F_VERSION

LOGGER = logging.getLogger("uvicorn")


def save_server_data_to_json():
    data = {"ip": SERVER_IP, "port": SERVER_PORT}
    api_json.json_to_file(data, "server_data.json")
    return


save_server_data_to_json()


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


from .message_item import GenerateImageItem, ChatItem, ResultItems
