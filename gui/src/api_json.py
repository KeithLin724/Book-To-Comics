import json


def json_to_file(json_obj, file_name: str):
    """
    The function `json_to_file` takes a JSON object and a file name as input, and writes the JSON object
    to a file with the given name.

    :param json_obj: The `json_obj` parameter is the JSON object that you want to write to a file. It
    can be any valid JSON object, such as a dictionary, list, or string
    :param file_name: The `file_name` parameter is a string that represents the name of the file where
    the JSON object will be saved
    :type file_name: str
    """
    if not file_name.endswith(".json"):
        file_name = f"{file_name}.json"

    with open(file=file_name, mode="w") as f:
        json.dump(json_obj, f)


def load_json_from_file(file_name: str):
    """
    The function `load_json_from_file` loads a JSON object from a file.

    :param file_name: The `file_name` parameter is a string that represents the name or path of the JSON
    file that you want to load
    :type file_name: str
    :return: a JSON object.
    """
    with open(file=file_name, mode="r") as f:
        json_object = json.load(f)
    return json_object
