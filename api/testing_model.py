import unittest
from stable_diffusion import TextToImage

import matplotlib.pyplot as plt


class TestTextToImage(unittest.TestCase):
    def test_is_run(self):
        textToImage = TextToImage()
        image = textToImage.generate("a photo of an astronaut riding a horse on mars")

        self.assertTrue(image)
        print(type(image))
        plt.imshow(image)
        plt.axis("off")  # Optionally, turn off the axis labels
        plt.show()


# if __name__ == "__main__":
#     unittest.main()
