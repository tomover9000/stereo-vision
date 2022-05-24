import requests
import cv2
import os

IMAGE_PATH = "C:\\Users\\vladz\\OneDrive - Universitatea Politehnica Bucuresti\\Licenta\\stereo-vision\\images\\"

cam1 = requests.get("http://192.168.0.145:5000/image1").content
cam2 = requests.get("http://192.168.0.145:5000/image2").content

print(type(cam1))

cv2.imshow("Video", cam1)