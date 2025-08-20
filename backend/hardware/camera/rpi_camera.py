import numpy as np #Essential because camera frame will be provieded as a NumPy array
from picamera2 import Picamera2 #Primary tool for interfacing with Raspi Cam

from backend.hardware.camera.base_camera import BaseCamera
from backend.utils.logging import logging_default


class RPiCamera(BaseCamera): #creates a new class named RPiCamera that inherits from BaseCamera
    def __init__(self):
        logging_default.info("Setting up the camera")
        self.picam2 = Picamera2() #creates an instance of the Picamera2 class, initializes the connection to the physical camera hardware
        self.picam2.start() # calls the .start() method on the camera object. This powers up the camera sensor and starts the video stream

    def get_capture(self) -> np.ndarray: #purpose is to capture a single, current frame from the camera's video stream
        try: #Error-Handling Mechanism
            frame = self.picam2.capture_array() #calls the .capture_array() method on the picam2 object, which grabs the latest frame from the video stream and returns it as a NumPy array
            if frame is not None:
                return True, frame
            logging_default.warning("PiCamera2 returned None")
        except Exception as e:
            logging_default.error(f"Error capturing frame image from Pi Camera 2: {e}")
        return False, None

    def release(self):
        pass
