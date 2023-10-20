from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from stable_diffusion import TextToImage
import g4f
import os
from multiprocessing import Process

app = Flask(__name__)

PORT_g4f = 1337

model = TextToImage()

FOLDER_PATH = "./tmp"


def init():
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    print(g4f.version)  # check version
    print(g4f.Provider.Ails.params)  # supported args
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/test")
def testing():
    web_URL = f"http://{request.remote_addr}:{PORT_g4f}"
    return f"testing, IP :{web_URL}"


@app.route("/chat", methods=["GET"])
def chat_to_ai():
    model = request.headers.get("model", "gpt-3.5-turbo")
    message = request.headers.get("message")

    return g4f.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )


def handle_user_folder(user_name) -> str:
    path = os.path.join(FOLDER_PATH, user_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


@app.route("/generate", methods=["GET"])
def generate_image():
    user_name = request.headers.get("name", "tmp")

    user_prompt = request.headers.get("prompt")
    if user_prompt is None:
        return "Does not send the prompt"

    user_save_folder_path = handle_user_folder(user_name=user_name)
    image = model.generate(prompt=user_prompt)

    file_path = os.path.join(user_save_folder_path, f"{user_prompt}.jpg")

    image.save(file_path)

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    model.load()
    init()
    app.run(host="0.0.0.0")
