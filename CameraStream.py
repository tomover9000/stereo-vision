import cv2

class CameraStream:
    def __init__(self, camera_id, width=1280, height=720, side='right') -> None:
        self.id = camera_id
        self.cam = cv2.VideoCapture(self.id)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # print("Camera status: ", self.cam.isOpened())

        # Camera parameters to undistort and rectify images
        cv_file = cv2.FileStorage()
        cv_file.open('stereoMap.xml', cv2.FileStorage_READ)

        if side == 'right':
            self.stereoMap_x = cv_file.getNode('stereoMapR_x').mat()
            self.stereoMap_y = cv_file.getNode('stereoMapR_y').mat()
        else:
            self.stereoMap_x = cv_file.getNode('stereoMapL_x').mat()
            self.stereoMap_y = cv_file.getNode('stereoMapL_y').mat()

    def gen_frames(self):  
        while True:
            success, frame = self.cam.read()  # read the camera frame
            if not success:
                break
            else:
                frame = cv2.remap(frame, self.stereoMap_x, self.stereoMap_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def get_frame(self):
        success, frame = self.cam.read()  # read the camera frame
        if not success:
            return
        else:
            return frame

    def __del__(self):
        self.cam.release()
