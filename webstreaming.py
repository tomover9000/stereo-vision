#Import necessary libraries
from crypt import methods
from flask import Flask, jsonify, render_template, Response, send_file, request
from CameraStream import CameraStream
from ImageOperations import ImageOperations
import numpy as np
import cv2
import base64

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

PROJECT_PATH = '/home/pi/actions-runner/_work/stereo-vision/stereo-vision/'

#Initialize the Flask app
app = Flask(__name__)
camera1 = CameraStream(0, CAMERA_WIDTH, CAMERA_HEIGHT)
camera2 = CameraStream(2, CAMERA_WIDTH, CAMERA_HEIGHT)
img_op = ImageOperations(camera1, camera2)

def decode_image(img_string):
    return cv2.imdecode(np.frombuffer(base64.b64decode(img_string), dtype=np.uint8), cv2.IMREAD_COLOR)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route("/video_feed1")
def video_feed1():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera1.gen_frames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed2")
def video_feed2():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera2.gen_frames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/processed_image')
def processed_image():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(img_op.gen_disp_map(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/', methods=['POST'])
def greet():
    if 'name' in request.form:
        name = request.form['name']
        return jsonify(message=f'Hello, {name}.')
    return '', 400
