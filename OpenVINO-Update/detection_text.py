# import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from datetime import datetime
import os
from models_init import *

# Define timestamp
timestamp = int(datetime.timestamp(datetime.now()))

# This is for matplotlib to display image
matplotlib.use('Agg')

# N,C,H,W = batch size, number of channels, height, width
N, C, H, W = input_keys_text.shape

# Resize image to meet network expected input sizes
def resize_image_text():
    resized_image = cv2.resize(image_show(), (W, H))
    return resized_image

# Reshape to network input shape
def reshape_image_text():
    input_image = np.expand_dims(resize_image_text().transpose(2, 0, 1), 0)
    return input_image

# Create inference request
def box_detect():
    boxes = compiled_model_text([reshape_image_text()])[output_keys_text]
    boxes = boxes[~np.all(boxes == 0, axis=1)]
    return boxes

# For each detection, the description has the format: [x_min, y_min, x_max, y_max, conf]
# Image passed here is in BGR format with changed width and height. To display it in colors expected by matplotlib we use cvtColor function
def convert_result_text(bgr_image, resized_image, boxes, threshold=0.3, conf_labels=True):
    # Define colors for boxes and descriptions
    colors = {"red": (255, 0, 0), "green": (0, 255, 0)}

    # Fetch image shapes to calculate ratio
    (real_y, real_x), (resized_y, resized_x) = bgr_image.shape[:2], resized_image.shape[:2]
    ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

    # Convert base image from bgr to rgb format
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

    # Iterate through non-zero boxes
    for box in boxes:
        # Pick confidence factor from last place in array
        conf = box[-1]
        if conf > threshold:
            # Convert float to int and multiply corner position of each box by x and y ratio
            # In case that bounding box is found at the top of the image,
            # we position upper box bar little lower to make it visible on image
            (x_min, y_min, x_max, y_max) = [
                int(max(corner_position * ratio_y, 10)) if idx % 2
                else int(corner_position * ratio_x)
                for idx, corner_position in enumerate(box[:-1])
            ]

            # Draw box based on position, parameters in rectangle function are: image, start_point, end_point, color, thickness
            rgb_image = cv2.rectangle(rgb_image, (x_min, y_min), (x_max, y_max), colors["green"], 3)

            # Add text to image based on position and confidence
            # Parameters in text function are: image, text, bottom-left_corner_textfield, font, font_scale, color, thickness, line_type
            if conf_labels:
                rgb_image = cv2.putText(
                    rgb_image,
                    f"{conf:.2f}",
                    (x_min, y_min - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    colors["red"],
                    1,
                    cv2.LINE_AA,
                )

    return rgb_image

# Display image
def show_image(raw_image):
    print("rendering image")
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.imshow(raw_image);
    plt.savefig("static/gallery/flask_text_%s.jpg" % timestamp)
    print("success")
