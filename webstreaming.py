#Import necessary libraries
from ast import Num
from crypt import methods
from flask import Flask, jsonify, render_template, Response, send_file, request
from CameraStream import CameraStream
from ImageOperations import ImageOperations
import numpy as np
import cv2
import base64
from time import sleep

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

PROJECT_PATH = '/home/pi/actions-runner/_work/stereo-vision/stereo-vision/'

#Initialize the Flask app
app = Flask(__name__)
camera1 = CameraStream(0, CAMERA_WIDTH, CAMERA_HEIGHT, side='left')
camera2 = CameraStream(2, CAMERA_WIDTH, CAMERA_HEIGHT, side='right')
img_op = ImageOperations(camera1, camera2)

def decode_image(img_string):
    return cv2.imdecode(np.frombuffer(base64.b64decode(img_string), dtype=np.uint8), cv2.IMREAD_COLOR)

@app.route("/", methods=["POST", "GET"])
def index():
	if request.method == "POST":
		MinDisparity = int(request.form.get("MinDisparity"))
		NumDisparities = int(request.form.get("NumDisparities"))
		BlockSize = int(request.form.get("BlockSize"))
		SpeckleRange = int(request.form.get("SpeckleRange"))
		SpeckleWindowSize = int(request.form.get("SpeckleWindowSize"))
		img_op.set_params(MinDisparity, NumDisparities, BlockSize, SpeckleRange, SpeckleWindowSize)
	# return the rendered template
	return render_template("index.html")

@app.route("/capture_calibration_photos")
def cap_calib_photos():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(img_op.capture_calib_photos(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

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

@app.route('/upload', methods=['POST'])
def upload():
    # Same cool stuff here.
    print(request.form.get('data'))

    return jsonify(message='success')
