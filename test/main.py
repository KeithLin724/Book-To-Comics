import requests
import json
from flask import jsonify
from rich import print as rPrint
import io
from PIL import Image
import matplotlib.pyplot as plt


data = {
    # "model": "gpt-4",
    "message": "please give me a prompt only replay json format like {prompt:...}",
}


resource = requests.get("http://140.113.89.60:5000/chat", headers=data)


print(resource.text)

resource = requests.get("http://140.113.89.60:5000/chat", headers=resource.json())


def to_Image(data: bytes):
    image_io = io.BytesIO(data)

    return Image.open(image_io)


def plt_image(image):
    plt.imshow(image)
    plt.axis("off")  # Optionally, turn off the axis labels
    plt.show()


plt_image(to_Image(resource.content))
