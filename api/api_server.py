from flask import Flask, send_file, request, jsonify, render_template, Response
import socket

# from flask_cors import CORS
from stable_diffusion import TextToImage
import g4f
import os
import time
import logging
from PIL import Image

from rq import Queue, get_current_job
from redis import Redis

from api_func import generate_image_queue


from copy import deepcopy
import rq_dashboard

import uuid
import datetime

app = Flask(__name__)
redis_connect = Redis(host="localhost", port=6379)
task_image_queue = Queue("generate-image-queue", connection=redis_connect)

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

model = TextToImage()
# taskQueue = TaskQueue()

FOLDER_PATH = "./image"
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5000

logger = logging.getLogger("werkzeug")  # grabs underlying WSGI logger
# handler = logging.FileHandler("test_server.log")  # creates handler for the log file
# logger.addHandler(handler)  # adds handler to the werkzeug WSGI logger


# function
def is_connect_redis():
    try:
        redis_connect.ping()  # This will check if the connection to Redis is alive
        print("Connected to Redis successfully.")
    except Exception as e:
        print(f"Failed to connect to Redis: {str(e)}")
        exit(-1)


def init():
    g4f.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking
    print(g4f.version)  # check version
    # print(g4f.Provider.Ails.params)  # supported args
    model.load()
    is_connect_redis()


@app.route("/")
def hello():
    return render_template("index.html", g4f_version=g4f.version)


@app.route("/redis-generate", methods=["POST"])
def redis_generate():
    data = request.get_json()


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

    # ! add the id in the generate_image , for make a only one file name
    # ! like user_name/{id}.png
    # ! generate_image not reply a file path , return a Image

    job = task_image_queue.enqueue(
        generate_image_queue,
        "http://140.113.89.60:5000/generate",
        {
            "name": user_name,
            "prompt": user_prompt,
        },
    )
    # result = generate_image.delay(user_name, user_prompt)
    return jsonify(
        {
            "task_id": job.get_id(),
            "queue_len": len(task_image_queue),
            "result-link": "test-result",
        }
    )


@app.route("/test-result", methods=["POST"])
def testing_result():
    error_reply = jsonify({"message": "we only accept format like {'task_id':'...'}"})

    if not request.data or not request.content_type.startswith("application/json"):
        return error_reply

    data = request.get_json()

    user_name = data.get("name", "tmp")

    user_task_id = data.get("task_id")
    if user_task_id is None:
        return error_reply

    the_job = task_image_queue.fetch_job(user_task_id)

    while not the_job.is_finished:
        time.sleep(1)

    result_image: Image = the_job.result

    file_path = handle_user_folder(user_name=user_name)

    file_path = os.path.join(file_path, f"{user_task_id}.png")

    result_image.save(file_path)

    return jsonify(
        {
            "file_path": file_path,
        }
    )


@app.route("/test-result", methods=["GET"])
def testing_image_return():
    return jsonify({"result", "not ready"})


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

    job = task_image_queue.enqueue(
        generate_image_queue,
        f"http://{SERVER_IP}:{SERVER_PORT}/generate-redis",
        {
            "name": user_name,
            "prompt": user_prompt,
        },
    )

    while not job.is_finished:
        time.sleep(1)

    result = job.result
    print(result.json())

    return result.json()


@app.route("/generate-redis", methods=["POST"])
def generate_image():
    """
    This is for the redis server send the request.

    The `generate_image` function generates an image based on user input, saves it with a unique file
    name, and returns the file information.
    :return: a JSON response. If the request data is missing or the content type is not in the expected
    format, it returns an error message. Otherwise, it generates an image based on the provided prompt
    using a model, saves the image to a file with a unique name, and returns a JSON object containing
    the unique ID, file path, file name, and current time.
    """
    error_reply = jsonify(
        {"message": "we only accept format like {'name':'...', 'prompt':'...'}"}
    )

    if not request.data or not request.content_type.startswith("application/json"):
        return error_reply

    data = request.get_json()

    user_name, user_prompt = data.get("name"), data.get("prompt")

    image = model.generate(prompt=user_prompt)

    now_time = datetime.datetime.now()

    # make a unique file name
    unique_file_name = uuid.uuid5(
        namespace=uuid.NAMESPACE_DNS,
        name=f"{user_name}_{user_prompt}_{now_time}",
    )

    file_path = handle_user_folder(user_name=user_name)

    file_path = os.path.join(file_path, f"{unique_file_name}.png")
    image.save(file_path)

    return jsonify(
        {
            "id": unique_file_name,
            "file_path": file_path,
            "file_name": f"{unique_file_name}.png",
            "time": now_time,
        }
    )


@app.route("/result", methods=["POST"])
def replay_image():
    error_reply = jsonify({"message": "we need the 'id' and the 'name' or 'file_path'"})

    if not request.data or not request.content_type.startswith("application/json"):
        return error_reply

    data: dict = request.get_json()

    file_path = data.get("file_path", None)

    # check the file path
    if file_path is not None and os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg", as_attachment=True)

    # check the user_name and the user_id is both exits
    user_name, user_id = data.get("name", None), data.get("id", None)
    if user_name is None or user_id is None:
        return jsonify({"message": "please summit the 'id' and 'name'"})

    # make the file path and check it
    file_path = os.path.join(FOLDER_PATH, user_name, f"{user_id}.png")
    if not os.path.exists(file_path):
        return jsonify({"message": "can not find the file about this id"})

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    init()

    app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
