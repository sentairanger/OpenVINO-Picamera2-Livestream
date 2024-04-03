# import libraries
from openvino.runtime import Core
import os
from typing import Tuple
import cv2

# initialize the engine
ie = Core()
# image
image_sample = "static/gallery/image.jpg"
## Base directory
base_directory = "models"
## Classification model
classification_directory = "classify"
classification_model = "v3-small_224_1.0_float.xml"
classification_text = "imagenet_2012.txt"
classification_path = os.path.join(base_directory, classification_directory, classification_model)
text_classification_path = os.path.join(base_directory, classification_directory, classification_text)
## Text detection model
text_directory = "text"
text_model = "horizontal-text-detection-0001.xml"
text_path = os.path.join(base_directory, text_directory, text_model)
## Vehicle models
vehicle_directory = "vehicle"
detection_model = "vehicle-detection-0200.xml"
recognition_model = "vehicle-attributes-recognition-barrier-0039.xml"
detection_path = os.path.join(base_directory, vehicle_directory, detection_model)
recognition_path= os.path.join(base_directory, vehicle_directory, recognition_model)

# initialize the models
def model_init(model_path: str) -> Tuple:
    model = ie.read_model(model=model_path)
    compiled_model = ie.compile_model(model=model, device_name="MYRIAD")
    try:
        output_keys = compiled_model.output(0)
    except AttributeError:
        output_keys = compiled_model.output("boxes")
    input_keys = compiled_model.input(0)
    return output_keys, input_keys, compiled_model

# Define the keys and the model
output_keys_classify, _, compiled_classified = model_init(classification_path)
output_keys_re, input_keys_re, compiled_model_re = model_init(recognition_path)
output_keys_de, input_keys_de, compiled_model_de = model_init(detection_path)
output_keys_text, input_keys_text, compiled_model_text = model_init(text_path)

# Read image
def image_show():
    image = cv2.imread(image_sample)
    return image
