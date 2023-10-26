from flask import Flask, render_template, request, jsonify
import logging
import requests
from api_json import load_json_from_file

app = Flask(__name__)
CLIENT_PORT = 7000
logger = logging.getLogger("werkzeug")


def init():
    global SERVER_URL
    data_json = load_json_from_file("./server_data.json")
    ip, port = data_json["IP"], data_json["port"]

    SERVER_URL = f"http://{ip}:{port}"

    return


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    # str_in = request.form.get("msg")
    data_in = request.get_json()
    str_in = data_in.get("msg")
    app.logger.info(msg=str_in)
    app.logger.debug(SERVER_URL)
    url = "/".join([SERVER_URL, "chat"])
    try:
        # 发出 GET 请求
        response = requests.post(url, json={"message": str_in})

        # 检查响应状态码
        if response.status_code == 200:
            # 成功获取数据
            data = response.json()
            return jsonify({"msg": data["message"]})

        else:
            return "Failed to get data from the server", 500

    except Exception as e:
        return jsonify({"msg": f"{str(e)} :state code 500"})


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", port=CLIENT_PORT, debug=True)
