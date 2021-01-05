# STEP 1: First, we need to ingest an image

from PIL import Image

IMG_CONVERTED_WIDTH = 224
IMG_CONVERTED_HEIGHT = 224
TEST_IMG_PATH = "/Volumes/Development/python3-lightspeed-gamma/Images/gucci-diamond-belt-900x610.jpg"

def show_image(img):
    return img.show()

def image_convert_to_uniform_size(img_data, new_width, new_height):
    return img_data.resize((new_width, new_height))

def ingest_image(path):
    img = Image.open(path)
    resized_img = image_convert_to_uniform_size(img, IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT)
    return resized_img

# Test everything above works
# show_image(ingest_image(TEST_IMG_PATH))