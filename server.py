import os
import json
import numpy as np
from PIL import Image
from argparse import ArgumentParser
import tensorflow as tf
import tensorflow_hub as hub
from annoy import AnnoyIndex
from io import BytesIO
from flask import Flask, jsonify, request, render_template, send_file, make_response
from get_image_embedding import load_model
from image_ingestion import resize_img, ingest_image_from_local_path, show_image
from build_index import build_index
from Constants import *

MODE = RUN_MODE.LOCAL_TERMINAL_TEST
IMG_PATH_TO_TEST = TEST_IMG_PATH

curModel = None
imgs_index = None

def get_model():
    global curModel
    if not curModel:
        curModel = load_model()
    return curModel

def get_index():
    global imgs_index
    if os.path.exists(INDX_FILE) and os.path.exists(INDX_METADATA_FILE):
        print("Index found!")
        annoyIndexInstance = AnnoyIndex(
            ANNOY_VECTOR_DIMENSIONS, 
            ANNOY_METRICS[ANNOY_METRIC_IN_USE-1]
        )
        annoyIndexInstance.load(INDX_FILE)
        annoyIndexMetadata = json.load(
            open(INDX_METADATA_FILE, READ_PERMISSIONS)
        )

        annoyIndexMetadata = {int(k): v for (k, v) in annoyIndexMetadata.items()}
    
    else:
        print("no index found!!! Building now")
        parser = ArgumentParser()
        parser.add_argument('--images-dir', type=str, default=IMG_DIR_IDX)
        parser.add_argument('--dst', type=str, default=INDX_DIR)
        parser.add_argument('--batch-size', type=int, default=NUM_IMAGES)
        parser.add_argument('--n-trees', type=int, default=10)
        parser.add_argument('--max-items', type=int, default=10000)

        annoyIndexInstance, annoyIndexMetadata = build_index(parser.parse_args())

    imgs_index = (annoyIndexInstance, annoyIndexMetadata)
    return imgs_index

def open_img_file(imgData):
    img = Image.open(BytesIO(imgData))
    return resize_img(img, IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT)

def get_image_feature_vector(img):
    model = get_model()
    return model(
        np.asarray(img).reshape(
            (INFER_DIMENSION_FROM_IMG, IMG_CONVERTED_WIDTH, IMG_CONVERTED_HEIGHT, COLOR_SPACE)
        )
    )[0]

def get_image_match():
    img = ingest_image_from_local_path(IMG_PATH_TO_TEST)
    img_feature_embedding_vector = get_image_feature_vector(img)
    print(img_feature_embedding_vector)
    
    # Next, build the index + retrieve in memory, if we dont already hold that as mmap
    index, index_metadata = get_index()
    
    ids = index.get_nns_by_vector(img_feature_embedding_vector, 1)
    resData = {'item matched': [{'id': id, 'metadata': index_metadata.get(id, None)} for id in ids]}
    image_matched_response = make_response(
        jsonify(resData)
    )

    # show response:
    if (RUN_MODE.LOCAL_TERMINAL_TEST):
        itemIdMatched = resData['item matched'][0]['id']
        imageNameMatched = resData['item matched'][0]['metadata']['fname']
        imgPathToOpen = IMG_DIR_IDX + str(imageNameMatched)
        
        print(json.loads(image_matched_response.data))
        print("This is the image for item id " + str(itemIdMatched) + " matched from the index: \n")
        
        img = Image.open(imgPathToOpen)
        show_image(img)

    return image_matched_response


# Utility
def print_in_flask(s):
    import sys
    print(str(s), file=sys.stdout)
    return


# Server Code:

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    print("Server is up :)")
    return render_template("index_image_upload.html")

if __name__ == "__main__":
    if (MODE == RUN_MODE.LOCAL_TERMINAL_TEST):
        with app.app_context():
            get_image_match()
    elif (MODE == RUN_MODE.LINK_TO_WEBSITE):
        app.run(debug=True)
    else:
        raise Exception("Invalid RUN_MODE specified, please specify the correct one at the top pf the server file.")