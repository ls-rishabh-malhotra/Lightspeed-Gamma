import enum
class RUN_MODE(enum.Enum):
   LOCAL_TERMINAL_TEST = "SERVER_OUTPUT_MODE"
   LINK_TO_WEBSITE = "WEBPAGE_MODE"

MODE = RUN_MODE.LOCAL_TERMINAL_TEST

FORCE_REBUILD_INDX = False
BUILD_INDX_SEPARATELY = False

READ_PERMISSIONS = 'r'
WRITE_PERMISSIONS = 'w'

ANNOY_VECTOR_DIMENSIONS = 2048
ANNOY_METRICS = ['angular', 'euclidean', 'manhattan', 'hamming', 'dot']
ANNOY_METRIC_IN_USE = 2     # Using 'Euclidean' distance to tally vector association

TFHUB_RESNET50_PRETRAINED_MODEL = "https://tfhub.dev/tensorflow/resnet_50/feature_vector/1"

IMG_CONVERTED_WIDTH = 224
IMG_CONVERTED_HEIGHT = 224
INFER_DIMENSION_FROM_IMG = -1
COLOR_SPACE = 3 #RGB

GAMMA_IDX = "/Volumes/Development/inno_weeks/Lightspeed-Gamma/"
IMG_DIR_IDX = GAMMA_IDX + "index_images/"
IMG_TEST_DIR = GAMMA_IDX + "test_images/"
QUERY_IMG_DIR = GAMMA_IDX + "query_images/"

INDX_DIR = "."
INDX_METADATA_FILE = 'index_metadata.json'
INDX_FILE = 'index.ann'

TEST_IMG_PATH = ""
IMG_PATH_TO_TEST = TEST_IMG_PATH

import os
NUM_IMAGES = len([name for name in os.listdir(IMG_DIR_IDX) if os.path.isfile(name)])


################  Google Cloud Configs  ################

PROJECT_ID = "ls-sandbox-dev"
SUBSCRIPTION_NAME = "client_activity-sub"
