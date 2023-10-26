from flask import Flask, render_template, request


app = Flask(__name__)
CLIENT_PORT = 7000


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    str_in = request.form.get("msg")

    return str_in


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=CLIENT_PORT, debug=True)
