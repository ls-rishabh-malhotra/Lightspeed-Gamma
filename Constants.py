READ_PERMISSIONS = 'r'
WRITE_PERMISSIONS = 'w'

ANNOY_VECTOR_DIMENSIONS = 2048
ANNOY_METRICS = ['angular', 'euclidean', 'manhattan', 'hamming', 'dot']
ANNOY_METRIC_IN_USE = 2

TFHUB_RESNET50_PRETRAINED_MODEL = "https://tfhub.dev/tensorflow/resnet_50/feature_vector/1"

IMG_CONVERTED_WIDTH = 224
IMG_CONVERTED_HEIGHT = 224
INFER_DIMENSION_FROM_IMG = -1
COLOR_SPACE = 3 #RGB

IMG_DIR_IDX = "/Volumes/Development/python3-lightspeed-gamma/index_images/"
IMG_TEST_DIR = "/Volumes/Development/python3-lightspeed-gamma/test_images/"
TEST_IMG_PATH = IMG_TEST_DIR + "gucci-diamond-belt-test.jpg"
TEST_IMG_PATH_2 = IMG_TEST_DIR + "gucci-diamond-belt-rotate-test.jpg"

INDX_DIR = "."
INDX_METADATA_FILE = 'index_metadata.json'
INDX_FILE = 'index.ann'

import os
NUM_IMAGES = len([name for name in os.listdir(IMG_DIR_IDX) if os.path.isfile(name)])