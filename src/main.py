import requests
import io
from PIL import Image
import matplotlib.pyplot as plt


# %%
response = requests.get("http://140.113.89.60:5000")
print(response.text)  # Print the content of the response

cmd = "cat is running"

response = requests.get(f"http://140.113.89.60:5000/generate/{cmd}")

# %%
print(response)


def to_Image(data: bytes):
    image_io = io.BytesIO(data)

    return Image.open(image_io)


image = to_Image(response.content)

plt.imshow(image)
plt.axis("off")  # Optionally, turn off the axis labels
plt.show()
