from flask import Flask, send_file, request
from stable_diffusion import TextToImage

import os

app = Flask(__name__)
model = TextToImage()

FOLDER_PATH = "./tmp"
if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/test", methods=["GET"])
def testing():
    name = request.headers.get("name")
    print(name)

    return f"testing, {name}"


def handle_user_folder(user_name) -> str:
    path = os.path.join(FOLDER_PATH, user_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


@app.route("/generate", methods=["GET"])
def generate_image():
    user_name = request.headers.get("name")
    if user_name is None:
        return "Does not send the user-name"

    user_prompt = request.headers.get("prompt")
    if user_prompt is None:
        return "Does not send the prompt"

    user_save_folder_path = handle_user_folder(user_name=user_name)
    image = model.generate(prompt=user_prompt)

    file_path = os.path.join(user_save_folder_path, f"{user_prompt}.jpg")

    image.save(file_path)

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


# @app.route("/generate/<string:user_prompt>", methods=["GET"])
# def make_image(user_prompt: str):
#     image = model.generate(prompt=user_prompt)
#     file_path = os.path.join(FOLDER_PATH, f"{user_prompt}.jpg")

#     image.save(file_path)

#     return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
