import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
from annoy import AnnoyIndex
from io import BytesIO
from flask import Flask, jsonify, request, render_template, send_file
from get_image_embedding import load_model
from image_ingestion import resize_img, ingest_image
from Constants import *

IMG_PATH_TO_TEST = TEST_IMG_PATH_2

curModel = None
imgs_index = None

def get_model():
    global curModel
    if not curModel:
        curModel = load_model()
    return curModel

def get_index():
    global imgs_index
    if not imgs_index:
        annoyIndexInstance = AnnoyIndex(
            ANNOY_VECTOR_DIMENSIONS, 
            ANNOY_METRICS[ANNOY_METRIC_IN_USE-1]
        )
        annoyIndexInstance.load(INDX_FILE)
        annoyIndexMetadata = json.load(
            open(INDX_METADATA_FILE, READ_PERMISSIONS)
        )

        annoyIndexMetadata = {int(k): v for (k, v) in annoyIndexMetadata.items()}
        imgs_index = (annoyIndexInstance, annoyIndexMetadata)
        
    return imgs_index

def get_image_feature_vector(img):
    model = get_model()
    return model(
        np.asarray(img).reshape(
            (INFER_DIMENSION_FROM_IMG, IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT, COLOR_SPACE)
        )
    )[0]

# Utility
def printstuff(s):
    import sys
    print(str(s), file=sys.stdout)
    return


def test_image_match():
    img = ingest_image(IMG_PATH_TO_TEST)
    img_feature_embedding_vector = get_image_feature_vector(img)
    print(img_feature_embedding_vector)
    
    # Next, build the index + retrieve in memory, if we dont already hold that as mmap
    index, _ = get_index()
    
    ids = index.get_nns_by_vector(img_feature_embedding_vector, 1)

    return ids



# Server Code:

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Server is up :)"



if __name__ == "__main__":
    # app.run(debug=True) # -> to run server, uncomment this and comment following lines. To test, leave as is
    with app.app_context():
        print(test_image_match())