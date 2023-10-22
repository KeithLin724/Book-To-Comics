import requests


FOLDER_PATH = "./image"


def generate_image_queue(connect_path: str, data: dict):
    res = requests.post(connect_path, json=data)

    return res
