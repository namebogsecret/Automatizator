#/src/images/save_img.py
from os import mkdir, makedirs
from os.path import dirname, exists, join
from requests import get
from logging import getLogger
from log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

imges_dir = 'files/imgs'
if not exists(imges_dir):
    mkdir(imges_dir)

def save_img(url: str, name: str):

    image_path = join(imges_dir,f"{name}.jpg")
    if(exists(image_path)):
        logger.info("Image already exists: %s", image_path)
        return image_path
    response = get(url)

    if response.status_code == 200:
        makedirs(dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(response.content)
        logger.info("Image saved: %s", image_path)
        return image_path
    else:
        logger.error("Error while saving image: %s", response.status_code)
        return "None"
    