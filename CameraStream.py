import cv2

class CameraStream:
    def __init__(self, camera_id) -> None:
        self.id = camera_id
        self.cam = cv2.VideoCapture(self.id)
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

    def __del__(self):
        self.cam.release()
