#!/bin/bash

echo "System starting ..."

# Start pose estimation system
nohup python3 tf-openpose/src/main.py --pose tumble --resolution=320x240 > tf-openpose.log &

# Start mmwave system
# The serial ports may be different on other computers, please change it yourself at below.
sudo nohup python3 mmwave/main.py /dev/ttyACM0 /dev/ttyACM1 > mmwave.log &

echo "System started."
