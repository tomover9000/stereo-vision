#Import necessary libraries
from flask import Flask, render_template, Response
from CameraStream import CameraStream
import cv2

#Initialize the Flask app
app = Flask(__name__)
camera = CameraStream(1)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(camera.gen_frames(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
    

