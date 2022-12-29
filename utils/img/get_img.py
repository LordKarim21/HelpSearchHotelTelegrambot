from requests import get
from PIL import Image


def get_image(url: str):
    image = Image.open(get(url, stream=True).raw)
    img = image.resize((160, 300), Image.ANTIALIAS)
    return img
