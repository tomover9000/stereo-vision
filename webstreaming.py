#Import necessary libraries
from flask import Flask, render_template, Response
from CameraStream import CameraStream
import cv2

#Initialize the Flask app
app = Flask(__name__)
camera1 = CameraStream(0)
camera2 = CameraStream(3)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route("/video_feed1")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera1.gen_frames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed2")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera2.gen_frames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
    

