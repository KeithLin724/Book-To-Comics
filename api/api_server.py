from flask import Flask, send_file, request, jsonify, render_template, Response

# from flask_cors import CORS
from stable_diffusion import TextToImage
import g4f
import os
import time
import logging
from PIL import Image

from rq import Queue, get_current_job
from redis import Redis

from api_func import generate_image
import pickle

from copy import deepcopy
import rq_dashboard

app = Flask(__name__)
redis_connect = Redis(host="localhost", port=6379)
task_image_queue = Queue("generate-image-queue", connection=redis_connect)

app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")

model = TextToImage()
# taskQueue = TaskQueue()

FOLDER_PATH = "./image"

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

    try:
        job = task_image_queue.enqueue(
            generate_image,
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
    except Exception as e:
        print(f"Error enqueuing job: {str(e)}")
        return jsonify({"error": "An error occurred while enqueuing the job"})


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


# def generate_image(user_name: str, prompt: str):
#     user_save_folder_path = handle_user_folder(user_name=user_name)
#     image = model.generate(prompt=prompt)

#     file_path = os.path.join(user_save_folder_path, f"{prompt}.jpg")

#     image.save(file_path)
#     return file_path


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

    user_save_folder_path = handle_user_folder(user_name=user_name)
    image = model.generate(prompt=user_prompt)

    file_path = os.path.join(user_save_folder_path, f"{user_prompt}.jpg")

    image.save(file_path)

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    init()

    app.run(host="0.0.0.0", debug=True)
