import requests
import cv2
import os
import numpy as np
import base64
from time import sleep

IMAGE_PATH = "C:\\Users\\vladz\\OneDrive - Universitatea Politehnica Bucuresti\\Licenta\\stereo-vision\\images\\"

def decode_image(img_string):
    return cv2.imdecode(np.frombuffer(base64.b64decode(img_string), dtype=np.uint8), cv2.IMREAD_COLOR)

def encode_image(img):
    ret, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('ascii')

while True:
    req = requests.get("http://192.168.0.145:5000/get_images").json()
    # print(type(req['img1']))
    img1 = decode_image(req['img1'])
    gray_txt = encode_image(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
    # cv2.imshow("GRAY IMG", gray)
    # cv2.waitKey(1)
    dict_to_send = {
        'img1': gray_txt
    }
    
    # print(type(dict_to_send['img1']))
    res = requests.post("http://192.168.0.145:5000/post_images", json=dict_to_send)