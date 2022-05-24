#Import necessary libraries
from flask import Flask, jsonify, render_template, Response, send_file
from CameraStream import CameraStream
import cv2

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

#Initialize the Flask app
app = Flask(__name__)
camera1 = CameraStream(0, CAMERA_WIDTH, CAMERA_HEIGHT)
camera2 = CameraStream(2, CAMERA_WIDTH, CAMERA_HEIGHT)

# @app.route("/")
# def index():
# 	# return the rendered template
# 	return render_template("index.html")

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
	img1 = camera1.get_frame()
	img2 = camera2.get_frame()

	return jsonify({
		'img1': img1,
		'img2': img2
	})
