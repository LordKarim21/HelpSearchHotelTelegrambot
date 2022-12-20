import requests
from PIL import Image


def get_image(url: str):
    image = Image.open(requests.get(url, stream=True).raw)
    img = image.resize((160, 300), Image.ANTIALIAS)
    return img