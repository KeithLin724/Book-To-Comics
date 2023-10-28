import socket
from model import TextToImage
import os
from rq import Queue
from redis import Redis

REDIS_CONNECT = Redis(host="localhost", port=6379)
TASK_IMAGE_QUEUE = Queue("generate-image-queue", connection=REDIS_CONNECT)

SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000

text_to_image_model = TextToImage()
text_to_image_model.load()

FOLDER_PATH = os.getcwd()
IMAGE_FOLDER_PATH = os.path.join(FOLDER_PATH, "images")


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
