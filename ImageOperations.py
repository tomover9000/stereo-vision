import cv2
import numpy as np
from CameraStream import CameraStream

class ImageOperations:
    def __init__(self, camera1, camera2) -> None:
        self.cam1 = camera1
        self.cam2 = camera2
        self.stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        self.stereo.setMinDisparity(4)
        self.stereo.setNumDisparities(128)
        self.stereo.setBlockSize(21)
        self.stereo.setSpeckleRange(16)
        self.stereo.setSpeckleWindowSize(45)
    
    def __del__(self):
        pass

    def gen_gray_img(self):
        while True:
            frame = self.cam2.get_frame()
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            ret, buffer = cv2.imencode('.jpg', img_gray)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def gen_disp_map(self):
        while True:
            imgR = self.cam1.get_frame()
            imgL = self.cam2.get_frame()
            imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
            imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)

            
            disparity = self.stereo.compute(imgL_gray, imgR_gray)
            ret, buffer = cv2.imencode('.jpg', disparity)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
