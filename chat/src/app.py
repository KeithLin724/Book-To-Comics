from flask import Flask, render_template, request, jsonify, send_file
import requests
from rq.job import Job
from redis import Redis

import logging
import io

from api_json import load_json_from_file


app = Flask(__name__)
CLIENT_PORT = 7000
logger = logging.getLogger("werkzeug")
redis_conn = Redis()


def init():
    global SERVER_URL
    data_json = load_json_from_file("./server_data.json")
    ip, port = data_json["ip"], data_json["port"]

    SERVER_URL = f"http://{ip}:{port}"

    return


def take_out_str(string: str, cmd: str) -> str:
    index = string.find(cmd)

    return string[index + len(cmd) :].strip()


@app.route("/")
def home():
    app.logger.debug(SERVER_URL)
    return render_template("index.html")


def chat_mode(prompt: str):
    url = "/".join([SERVER_URL, "chat"])
    try:
        # 发出 GET 请求
        response = requests.post(url, json={"message": prompt})

        # 检查响应状态码
        if response.status_code == 200:
            # 成功获取数据
            data = response.json()
            return jsonify({"msg": data["message"]})

        else:
            # return "Failed to get data from the server", 500
            return jsonify(
                {"msg": "Failed to get data from the server :state code 500"}
            )

    except Exception as e:
        return jsonify({"msg": f"{str(e)} :state code 500"})


def generate_image_mode(prompt: str):
    prompt = take_out_str(string=prompt, cmd="generate image")
    url = "/".join([SERVER_URL, "generate"])

    try:
        # 发出 GET 请求
        response = requests.post(url, json={"prompt": prompt})

        # 检查响应状态码
        if response.status_code == 200:
            # 成功获取数据
            data = response.json()

            app.logger.info(f"get data: {data}")
            dis = {"msg": "catch it", "task_id": data.get("task_id")}
            app.logger.info(f"display :{dis}")

            return jsonify(dis)

        else:
            # return "Failed to get data from the server", 500
            return jsonify(
                {"msg": "Failed to get data from the server :state code 500"}
            )

    except Exception as e:
        return jsonify({"msg": f"{str(e)} :state code 500"})


def test(cmd: str):
    prompt = take_out_str(string=cmd, cmd="test")

    url = "/".join([SERVER_URL, "test"])
    app.logger.info(url)
    try:
        # 发出 GET 请求
        response = requests.post(url, json={"prompt": prompt})

        # 检查响应状态码
        if response.status_code == 200:
            # 成功获取数据
            data = response.json()

            app.logger.info(f"get data: {data}")
            dis = {"msg": "catch it", "task_id": data.get("task_id")}
            app.logger.info(f"display :{dis}")

            return jsonify(dis)

        else:
            # return "Failed to get data from the server", 500
            return jsonify(
                {"msg": "Failed to get data from the server :state code 500"}
            )

    except Exception as e:
        return jsonify({"msg": f"{str(e)} :state code 500"})


@app.route("/get", methods=["GET", "POST"])
def chat():
    # str_in = request.form.get("msg")
    data_in = request.get_json()
    prompt: str = data_in.get("msg")

    app.logger.info(msg=prompt)

    if "generate image" in prompt:
        return generate_image_mode(prompt=prompt)

    elif "test" in prompt:
        return test(cmd=prompt)

    else:
        return chat_mode(prompt=prompt)


@app.route("/check_image_state", methods=["GET"])
def check_image_state():
    # data = request.get_json()
    task_id = request.args.get("task_id")

    if not task_id:
        return jsonify({"error": "no task_id provided"})

    job = Job.fetch(task_id, connection=redis_conn)

    job_state, job_result = job.get_status(), job.result

    job_result = job_result.json() if job_result is not None else ""

    return jsonify(
        {
            "state": job_state,
            "result": job_result,
        }
    )


@app.route("/image-result", methods=["POST"])
def image_result():
    url = "/".join([SERVER_URL, "result"])

    data = request.get_json()

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # 成功获取数据
        app.logger.info(f"get image :{data}")
        image_bytes = io.BytesIO(response.content)

        file_name = data.get("id", "tmp")
        return send_file(
            path_or_file=image_bytes,
            mimetype="image/jpeg",
            as_attachment=True,
            download_name=f"{file_name}.jpg",
        )

    else:
        return jsonify({"msg": "Failed to get data from the server :state code 500"})


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=CLIENT_PORT)  # , debug=True
