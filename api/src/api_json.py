import json


def json_to_file(json_obj, file_name: str):
    if not file_name.endswith(".json"):
        file_name = f"{file_name}.json"

    with open(file=file_name, mode="w") as f:
        json.dump(json_obj, f)


def load_json_from_file(file_name: str):
    with open(file=file_name, mode="r") as f:
        json_object = json.load(f)
    return json_object
