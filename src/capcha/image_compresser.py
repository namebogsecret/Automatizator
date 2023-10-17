
import os
import argparse
from logging import getLogger
from PIL import Image

from src.log_scripts import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def compress_image(image_path, max_size=(400, 150), quality=90):
    image = Image.open(image_path)

    # Resize image to within max dimensions
    image.thumbnail(max_size)

    # Set up save path
    save_path = os.path.splitext(image_path)[0] + ".png"

    # Try to save the image
    for i in range(10):
        try:
            image.save(save_path, "PNG", quality=quality, 
            optimize=True, progressive=True)
        except IOError:
            quality -= 10
            continue
        break

    # Check the size of the output file, if it's still over 100kb reduce the quality
    file_size = os.stat(save_path).st_size

    if file_size > 100 * 1024:
        compress_image(save_path, max_size, quality-10)
    else:
        return save_path


def compress_image2(image_path, max_size=(400, 150), file_size_limit=100 * 1024):
    #logger.info("Сжатие изображения")
    original_image = Image.open(image_path)
    width, height = original_image.size
    aspect_ratio = width / height

    save_path = os.path.splitext(image_path)[0] + ".png"

    for size_increase in range(0, 100):
        new_width = max_size[0] + size_increase
        new_height = int(new_width / aspect_ratio)

        if new_height > max_size[1]:
            new_height = max_size[1]
            new_width = int(new_height * aspect_ratio)

        image = original_image.resize((new_width, new_height))
        image.save(save_path, "PNG", optimize=True, progressive=True)

        file_size = os.stat(save_path).st_size

        if file_size > file_size_limit:
            # If file size is too large, reduce the size and break the loop
            new_width -= 1
            new_height = int(new_width / aspect_ratio)
            image = original_image.resize((new_width, new_height))
            image.save(save_path, "PNG", optimize=True, progressive=True)
            break
    #logger.info("Изображение сжато")
    return save_path

def compress_image3_(image_path, max_size=(400, 150), file_size_limit=100 * 1024):
    logger.info("Сжатие изображения")
    original_image = Image.open(image_path)
    width, height = original_image.size
    aspect_ratio = width / height

    save_path = os.path.splitext(image_path)[0] + ".png"

    if max_size:
        # Initial resizing based on the aspect ratio and max_size
        if aspect_ratio > (max_size[0] / max_size[1]):
            new_width = max_size[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_size[1]
            new_width = int(new_height * aspect_ratio)
        
        image = original_image.resize((new_width, new_height))
        image.save(save_path, "PNG", optimize=True, progressive=True)

    else:
        # If max_size is None, just save the original image to get its size
        original_image.save(save_path, "PNG", optimize=True, progressive=True)
        

    file_size = os.stat(save_path).st_size

    # Further adjustments if the file size exceeds the limit
    while file_size > file_size_limit:
        new_width -= 1
        new_height = int(new_width / aspect_ratio)
        image = original_image.resize((new_width, new_height))
        image.save(save_path, "PNG", optimize=True, progressive=True)
        file_size = os.stat(save_path).st_size

    logger.info("Изображение сжато")
    return save_path

def compress_image3(image_path, max_size=(400, 150), file_size_limit=100 * 1024):
    logger.info("Сжатие изображения")
    original_image = Image.open(image_path)
    width, height = original_image.size
    aspect_ratio = width / height

    save_path = os.path.splitext(image_path)[0] + ".png"

    if max_size:
        # Initial resizing based on the aspect ratio and max_size
        if aspect_ratio > (max_size[0] / max_size[1]):
            new_width = max_size[0]
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_size[1]
            new_width = int(new_height * aspect_ratio)
        
        image = original_image.resize((new_width, new_height))
        image.save(save_path, "PNG", optimize=True, progressive=True)

    else:
        # If max_size is None, just save the original image to get its size
        original_image.save(save_path, "PNG", optimize=True, progressive=True)
        

    file_size = os.stat(save_path).st_size

    step = max(new_width, new_height) // 10  # уменьшим изначально на 10% от 
    #самой большой стороны

    while file_size > file_size_limit:
        new_width -= step
        new_height = int(new_width / aspect_ratio)
        image = original_image.resize((new_width, new_height))
        image.save(save_path, "PNG", optimize=True, progressive=True)
        file_size = os.stat(save_path).st_size
        
        if step > 1 and file_size < 1.2 * file_size_limit:  # когда мы приближаемся к
            # нужному размеру, делаем шаг меньше
            step //= 2

    logger.info("Изображение сжато")
    return save_path

if __name__ == "__main__":
     # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("ImagePath", help = "Path to the image file")

    # Read arguments from command line
    #args = parser.parse_args()

    #if not os.path.exists(ImagePath):
    print(compress_image3("instructions.png"))
    exit()
    #else:# Use the function
        #print(compress_image3(args.ImagePath))

    