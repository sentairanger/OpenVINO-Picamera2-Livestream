# OpenVINO-Picamera2-Livestream
This livestream UI uses picamera2 to take images and the OpenVINO toolkit to detect text, classify images and recognize vehicles. The camera is mounted on a robot so that the robot can see everything in front of it.

## Getting Started

To get started first you will need a Pi. This project was tested with the Pi 4 using Bullseye and this should also work with the 3B+. I have not tested it with the Pi 5 but once I get my hands on it I will test it using Bookworm. Next, you will need a Pi Camera module (any will suffice) but do not enable legacy stack mode. The code listed has code for a robot, but you can alter it so you can use a telescope especially if it's motorized. Next, you will need the Intel NCS2 which you can find from vendors like eBay. Next, you will have to install the OpenVINO toolkit so be sure to follow this [gist](https://gist.github.com/sentairanger/caf11a2432ceebd715c6b33c224f4960). After everything is set up you can start.

## Running The Code

Be sure to insert the NCS2 on the USB port on the Pi first and be sure you have everything else set up. Once you are ready, you can run the code with `python3 app.py`. You can do this using either your PC, Mac, phone or Tablet (if using an SSH client on iOS or Android). Go to `ip-address-of-pi:5000`. The image below shows what the UI should look like. You can view the video feed, take an image and then classify the image, detect text or recognize the vehicle. 

# New 2025 Update

I have added `OpenVINO-Update` to allow users to run the application using the latest version of OpenVINO. However, since the NCS2 will not work all the inferencing will be done by the CPU. To do this, it's best to install OpenVINO using pip. To do this create a virtual environment with `python3 venv -m venv`. You can then activate with `source venv/bin/activate`. After that run the application as usual. This application is best suited for the Raspberry Pi 4, 5, CM4, and the new CM5. The installation method I provided for the NCS2 only works for the older version of OpenVINO. This new installation method should work for any Pi, but due to RAM and CPU speeds, it's best to use the boards I have listed. 

![image](https://github.com/sentairanger/OpenVINO-Picamera2-Livestream/blob/main/Screenshot%20from%202024-04-01%2013-13-48.png)
