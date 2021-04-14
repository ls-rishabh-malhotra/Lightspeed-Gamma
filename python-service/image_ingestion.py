from PIL import Image
from Constants import IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT, TEST_IMG_PATH

# Utility
def show_image(img):
    return img.show()

def resize_img(img_data, new_width, new_height):
    return img_data.resize((new_width, new_height))

def ingest_image_from_local_path(path):
    img = Image.open(path)
    resized_img = resize_img(img, IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT)
    return resized_img