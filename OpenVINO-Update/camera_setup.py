import logging
from threading import Condition
from time import sleep
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import io
import os

# Define the camera
picam2 = Picamera2()

# Define the configuarion for video
video_config = picam2.create_video_configuration(main={"size": (640, 480)})

##################
# Streaming Class
##################

output = None

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

def generate():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\nContent-Type:image/jpeg\r\n\r\n' + frame + b'\r\n')

#############################
# Take image and start stream
#############################

def start_stream():
    global picam2, output, video_config
    picam2.configure(video_config)
    output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(output))
    metadata = picam2.capture_metadata()
    sleep(1)

def take_photo():
    try:
        image_name = "image"
        data_directory = "static/gallery"
        filepath = os.path.join(data_directory, image_name)
        request = picam2.capture_request()
        request.save("main", f'{filepath}.jpg')
        request.release()
        logging.info("image taken successfully")
    except Exception as e:
        logging.error(f"Error taking image: {e}")