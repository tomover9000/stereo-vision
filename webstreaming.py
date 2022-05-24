#Import necessary libraries
from crypt import methods
from flask import Flask, jsonify, render_template, Response, send_file, request
from CameraStream import CameraStream
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


def decode_image(img_string):
    return cv2.imdecode(np.frombuffer(base64.b64decode(img_string), dtype=np.uint8), cv2.IMREAD_COLOR)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

# @app.route("/video_feed1")
# def video_feed1():
# 	# return the response generated along with the specific media
# 	# type (mime type)
# 	return Response(camera1.gen_frames(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")

# @app.route("/video_feed2")
# def video_feed2():
# 	# return the response generated along with the specific media
# 	# type (mime type)
# 	return Response(camera2.gen_frames(),
# 		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/get_images")
def get_images():
	img1_text = base64.b64encode(camera1.get_frame())
	img2_text = base64.b64encode(camera2.get_frame())

	return jsonify({
		'img1': img1_text,
		'img2': img2_text
	})

@app.route("/post_images", methods=['POST'])
def post_images():
	input_json = request.get_json(force=True)
	img1 = decode_image(input_json['img1'])
	cv2.imwrite(PROJECT_PATH + 'images/img1.jpg', img1)
	dict_returned = {'state': 200}
	return jsonify(dict_returned)

