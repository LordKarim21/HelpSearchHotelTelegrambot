from requests import get
from PIL import Image


def get_image(url: str):
    image = Image.open(get(url, stream=True).raw)
    return image
