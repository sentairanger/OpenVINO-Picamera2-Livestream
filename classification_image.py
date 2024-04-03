# Import libraries
import cv2
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from models_init import *

# This is for matplotlib to run 
matplotlib.use('Agg')

# classify image
def classify_image():
    image = cv2.cvtColor(cv2.imread('static/gallery/image.jpg'), code=cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(src=image, dsize=(224,224))
    input_image = np.expand_dims(input_image, 0)
    result_infer = compiled_classified([input_image])[output_keys_classify]
    result_index = np.argmax(result_infer)
    imagenet_classes = open(text_classification_path).read().splitlines()
    imagenet_classes = ['background'] + imagenet_classes
    text = str(imagenet_classes[result_index])
    return text
