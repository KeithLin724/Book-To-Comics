from flask import Flask, send_file
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


@app.route("/generate/<string:user_prompt>", methods=["GET"])
def make_image(user_prompt: str):
    image = model.generate(prompt=user_prompt)
    file_path = os.path.join(FOLDER_PATH, f"{user_prompt}.jpg")

    image.save(file_path)

    return send_file(file_path, mimetype="image/jpeg", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
