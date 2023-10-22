import io
from PIL import Image


def image_to_bytes(image):
    """
    The function `image_to_bytes` converts an image object into a byte array.

    :param image: The "image" parameter is expected to be a PIL (Python Imaging Library) image object
    :return: the image data as bytes.
    """
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="JPEG")
    img_data = img_byte_array.getvalue()
    img_byte_array.close()
    return img_data


def bytes_to_image(bytes_of_image):
    """
    The function `bytes_to_image` converts a byte array representing an image into an Image object.

    :param bytes_of_image: The parameter `bytes_of_image` is expected to be a byte array that represents
    an image
    :return: an Image object.
    """
    img_byte_array = io.BytesIO(bytes_of_image)
    return Image.open(img_byte_array)
