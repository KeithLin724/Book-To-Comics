import requests
import io
from PIL import Image
import matplotlib.pyplot as plt
import unittest


def to_Image(data: bytes):
    image_io = io.BytesIO(data)

    return Image.open(image_io)


class ApiTesting(unittest.TestCase):
    def test_api(self):
        response = requests.get("http://172.18.145.128:5000")
        self.assertEqual(response.text, "Hello, World!")
        return

    def test_api_have_header(self):
        header = {"name": "KY"}
        response = requests.get("http://172.18.145.128:5000/test", headers=header)
        self.assertEqual(response.text, "testing, KY")

    def test_api_generate(self):
        header = {
            "name": "KY",
            "prompt": "cat is running",
        }
        response = requests.get("http://172.18.145.128:5000/generate", headers=header)
        self.assertTrue(response)

        image = to_Image(response.content)

        plt.imshow(image)
        plt.axis("off")  # Optionally, turn off the axis labels
        plt.show()


if __name__ == "__main__":
    unittest.main(verbosity=2)
