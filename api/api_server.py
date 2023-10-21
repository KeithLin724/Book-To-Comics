from flask import Flask, send_file, request, jsonify, render_template, Response

# from flask_cors import CORS
from stable_diffusion import TextToImage
import g4f
import os
import logging
from PIL import Image


from celery import Celery
from celery.result import AsyncResult

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

model = TextToImage()
# taskQueue = TaskQueue()

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
    model.load()
    # taskQueue.init()


@app.route("/")
def hello():
    return render_template("index.html", g4f_version=g4f.version)


@app.route("/test", methods=["POST"])
def testing():
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

    result = generate_image.delay(user_name, user_prompt)
    return jsonify({"task_id": result.id})


@app.route("/test-result", methods=["POST"])
def testing_result():
    error_reply = jsonify({"message": "we only accept format like {'task_id':'...'}"})

    if not request.data or not request.content_type.startswith("application/json"):
        return error_reply

    data = request.get_json()

    user_task_id = data.get("task_id")
    if user_task_id is None:
        return error_reply

    res = AsyncResult(user_task_id, app=celery)

    return jsonify({"result", res.result})


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


@celery.task(name="generate_image_task")
def generate_image(user_name: str, prompt: str):
    user_save_folder_path = handle_user_folder(user_name=user_name)
    image = model.generate(prompt=prompt)

    file_path = os.path.join(user_save_folder_path, f"{prompt}.jpg")

    image.save(file_path)
    return file_path


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


def run_api():
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    init()

    app.run(host="0.0.0.0", debug=True)
