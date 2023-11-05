import os
import socket
from . import api_func, api_json

# import api_json
from stable_diffusion import TextToImage
import logging
from redis import Redis

LAB_SERVER_IP = "140.113.238.35"
REDIS_CONNECT = Redis(host=LAB_SERVER_IP, port=6379)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 8060
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")
LOGGER = logging.getLogger("uvicorn")

text_to_image_model = TextToImage()
text_to_image_model.load()


def save_server_data_to_json():
    data = {
        "ip": SERVER_IP,
        "port": SERVER_PORT,
        "url": SERVER_URL,
    }
    api_json.json_to_file(data, "server_data(text_to_image).json")
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