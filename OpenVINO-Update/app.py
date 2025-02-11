# import libraries
from flask import Flask, request, render_template, jsonify, Response
from time import sleep
from camera_setup import *
from classification_image import classify_image
from detection_text import *
from detection_vehicle import *
from gpiozero import LED, Robot
import logging
import os

# define LED and robot
eye = LED(25)
robot = Robot(left=(13, 21), right=(17, 27))

# define the app
app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'static/gallery'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# main rote and routes for the LED and robot
@app.route("/")
def index():
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/on")
def eye_on():
    eye.on()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/off")
def eye_off():
    eye.off()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/forward")
def forward():
    robot.backward()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/backward")
def backward():
    robot.forward()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/left")
def left():
    robot.left()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/right")
def right():
    robot.right()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

@app.route("/stop")
def stop():
    robot.stop()
    return render_template("index.html", title="OpenVINO Picamera2 Livestream UI")

# About page
@app.route("/about")
def about():
    return render_template("about.html", title="About OpenVINO Picamera2 Livestream UI")
    
# data page
@app.route("/dataimage")
def data_image():
    try:
        image_name = 'image.jpg'
        image_file = os.path.join(UPLOAD_FOLDER, image_name)
        if os.path.exists(image_file):
            return render_template("data.html", image_file=image_file)
        else:
            return render_template("no_files.html")
    except Exception as ex:
        logging.error(f"Error in finding images:{ex}")
        return render_template("error.html")

# gallery page
@app.route("/gallery")
def gallery():
    try:
        image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.jpg'))]
        if not image_files:
            return render_template("no_files.html")
        ## Add dictionaries
        files = []
        for image_file in image_files:
            files.append({'filename': image_file})
        return render_template("gallery.html", image_files=files)
    except Exception as ex:
        logging.error(f"Error in finding images: {ex}")
        return render_template("error.html")

# capture image
@app.route("/capture", methods=['POST'])
def capture_photo():
    try:
        take_photo()
        sleep(1)
        return jsonify(success=True, message="Photo captured successfully")
    except Exception as e:
        return jsonify(success=False, message=str(e))

# Delete images
@app.route("/delete_image/<filename>", methods=['DELETE'])
def delete_image(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
        return jsonify(success=True, message="Image deleted successfully")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

# Display feed
@app.route("/videofeed")
def videofeed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# classify image
@app.route("/classify", methods=['POST'])
def classify():
    try:
        classify_string = str(classify_image())
        return jsonify(success=True, message=str(classify_string))
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

# detect text
@app.route("/detect", methods=['POST'])
def detect_text():
    try:
        show_image(convert_result_text(image_show(), resize_image_text(), box_detect(), conf_labels=False))
        text_string = "text rendered"
        return jsonify(success=True, message=str(text_string))
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

# detect vehicle
@app.route("/vehicle", methods=['POST'])
def vehicle_detection():
    try:
        plt_show(convert_result_vehicle(compiled_model_re, image_show(), resize_image_vehicle(), box_car()))
        vehicle_string = "vehicle detected"
        return jsonify(success=True, message=str(vehicle_string))
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

# Start logging, enable stream and run app
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_stream()
    app.run(host="0.0.0.0")
