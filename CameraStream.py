import cv2

class CameraStream:
    def __init__(self, camera_id, width=1280, height=720) -> None:
        self.id = camera_id
        self.cam = cv2.VideoCapture(self.id)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print("Camera status: ", self.cam.isOpened())

    def gen_frames(self):  
        while True:
            success, frame = self.cam.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    
    def get_frame(self):
        success, frame = self.cam.read()  # read the camera frame
        print(type(frame))
        if not success:
            return
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer

    def __del__(self):
        self.cam.release()
