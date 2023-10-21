from flask import Flask, send_file, request, jsonify, render_template, Response

# from flask_cors import CORS
from stable_diffusion import TextToImage
import g4f
import os
import logging
from PIL import Image
from requests_toolbelt import MultipartEncoder

# from celery import Celery

# from multiprocessing import Process

app = Flask(__name__)


model = TextToImage()

FOLDER_PATH = "./image"

logger = logging.getLogger("werkzeug")  # grabs underlying WSGI logger
# handler = logging.FileHandler("test_server.log")  # creates handler for the log file
# logger.addHandler(handler)  # adds handler to the werkzeug WSGI logger


# function


def init():
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    print(g4f.version)  # check version
    # print(g4f.Provider.Ails.params)  # supported args
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)


@app.route("/")
def hello():
    return render_template("index.html", g4f_version=g4f.version)


@app.route("/test", methods=["POST"])
def testing():
    # file_path = "./image/tmp/Write a short story about a mysterious package that arrives at your doorstep..jpg"
    # send_file(file_path, mimetype="image/jpeg", as_attachment=True)
    if request.content_type.startswith("application/json"):
        print(request.headers.get("Content-Type"))
        print(request.get_json())
    return "OK"


@app.route("/chat", methods=["POST"])
def chat_to_ai():
    if not request.data or not request.content_type.startswith("application/json"):
        return jsonify(
            {"message": "we only accept format like {'model':'...', 'message':'...'}"}
        )

    data = request.get_json()
    model = data.get("model", "gpt-3.5-turbo")
    message = data.get("message")

    reply_message = g4f.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    return jsonify({"message": reply_message})


def handle_user_folder(user_name) -> str:
    path = os.path.join(FOLDER_PATH, user_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


@app.route("/result")
def replay_image():
    return


@app.route("/generate", methods=["POST"])
def generate_image_request():
    error_reply = jsonify(
        {"message": "we only accept format like {'name':'...', 'prompt':'...'}"}
    )

    if not request.data or not request.content_type.startswith("application/json"):
        return error_reply

    data = request.get_json()

    user_name = data.get("name", "tmp")

    user_prompt = data.get("prompt")
    if user_prompt is None:
        return error_reply

    # 1 put the image to queue
    # 2

    user_save_folder_path = handle_user_folder(user_name=user_name)
    image = model.generate(prompt=user_prompt)

    file_path = os.path.join(user_save_folder_path, f"{user_prompt}.jpg")

    image.save(file_path)

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    model.load()
    init()
    app.run(host="0.0.0.0", debug=True)
