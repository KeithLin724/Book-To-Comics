from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)
CLIENT_PORT = 7000
logger = logging.getLogger("werkzeug")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    # str_in = request.form.get("msg")
    data_in = request.get_json()
    str_in = data_in.get("msg")
    app.logger.info(msg=str_in)
    return jsonify({"msg": str_in})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CLIENT_PORT, debug=True)
