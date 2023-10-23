import requests


def generate_image_queue(connect_path: str, data: dict):
    """
    For redis queue

    The function `generate_image_queue` sends a POST request to a specified path with JSON data and
    returns the response.

    :param connect_path: The `connect_path` parameter is a string that represents the URL or endpoint
    where the request will be sent to. It is the path to connect to the server or API
    :type connect_path: str
    :param data: The `data` parameter is a dictionary that contains the data to be sent in the request
    body as JSON
    :type data: dict
    :return: the response object from the POST request made to the specified `connect_path` with the
    provided `data` as JSON payload.
    """
    try:
        res = requests.post(connect_path, json=data)
        return res
    except Exception as e:
        return str(e)
