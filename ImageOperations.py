import cv2
import numpy as np
from CameraStream import CameraStream

class ImageOperations:
    def __init__(self, camera1, camera2) -> None:
        self.cam1 = camera1
        self.cam2 = camera2
    
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
