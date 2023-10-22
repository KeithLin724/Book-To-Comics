import requests


FOLDER_PATH = "./image"


def generate_image(connect_path: str, data: dict):
    # user_save_folder_path = handle_user_folder(user_name=user_name)
    # from stable_diffusion import TextToImage

    # model_api = TextToImage()
    # model_api.load()
    res = requests.post(connect_path, json=data)
    # file_path = os.path.join(user_save_folder_path, f"{prompt}.jpg")

    # image.save(file_path)
    return "OK"
