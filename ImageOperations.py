import cv2
import numpy as np
from CameraStream import CameraStream
from webstreaming import PROJECT_PATH
from time import sleep

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

    def set_params(self, MinDisparity, NumDisparities, BlockSize, SpeckleRange, SpeckleWindowSize):
        self.stereo.setMinDisparity(MinDisparity)
        self.stereo.setNumDisparities(NumDisparities)
        self.stereo.setBlockSize(BlockSize)
        self.stereo.setSpeckleRange(SpeckleRange)
        self.stereo.setSpeckleWindowSize(SpeckleWindowSize)

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
            imgL = self.cam1.get_frame()
            imgR = self.cam2.get_frame()
            imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
            imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)

            disparity = self.stereo.compute(imgL_gray, imgR_gray)
            ret, buffer = cv2.imencode('.jpg', disparity)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


    def capture_calib_photos(self):
        for i in range(1, 12):
            left_cam = self.cam1.get_frame()
            right_cam = self.cam2.get_frame()

            cv2.imwrite(PROJECT_PATH + "data/stereoL/img%d.png"%i, left_cam)
            cv2.imwrite(PROJECT_PATH + "data/stereoR/img%d.png"%i, right_cam)

            sleep(1)

            print("wrinting pictures for calibration no {}", i)

            ret, buffer = cv2.imencode('.jpg', left_cam)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result