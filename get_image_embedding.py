# Converts ingested image to its vector representation using a pre-trained 
# resnet_50 CNN. (50 layers). We will later attempt boosting accuracy by using
# a pre-trained(ImageNet), high accuracy model using VGG16.

# The goal here is to generate vector embeddings for an image, for which we are 
# hacking a Deep Neural Network. The strategy is to make the DNN "think" that we 
# simply want to use it for forward propagation ie for inference(which is why we 
# are picking up a highly accurate pre-trained DNN model with millions of images).
# But, when we start our inference by passing in our image, we will sneakily stop 
# the inference at the second-last last layer BEFORE the DNN has a chance to reach 
# the inference layer and unwrap the values of the activations the DNN has assigned
# so far!!


import tensorflow as tf
import tensorflow_hub as tf_hub
import numpy as np
from Constants import TFHUB_RESNET50_PRETRAINED_MODEL

# We want the most accurate cast here, so we use a float32 which provides 
# reasonably high decimal accuracy. This will be useful in avoiding common 
# pitfalls like the dead neuron issue.
def convert_img_datatype_float32(img):
    return tf.image.convert_image_dtype(img, tf.float32)

def load_model():
    resnet50Layer = tf.keras.layers.Lambda(lambda x: convert_img_datatype_float32(x))
    kerasLayer = tf_hub.KerasLayer(TFHUB_RESNET50_PRETRAINED_MODEL, trainable=False)
    linear_layers_stacked_model = tf.keras.Sequential([
        resnet50Layer,
        kerasLayer
    ])
    return linear_layers_stacked_model

# Cast every element of a list to npaarray
def cast_nparray(lst):
    return list(map(lambda x: np.asarray(x), lst))

# Can also be mutated to ingest multiple imgs
def generate_image_feature_vectors(model, imgs):
    np_imgs_stack = np.stack(
        cast_nparray(imgs)
        )
    return model(np_imgs_stack)