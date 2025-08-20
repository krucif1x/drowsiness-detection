import cv2 #a powerful tool for computer vision tasks, including capturing video from cameras
import numpy as np #essential because OpenCV represents image frames as NumPy arrays

from backend.hardware.camera.base_camera import BaseCamera #Imports the BaseCamera abstract class
from backend.utils.logging import logging_default #Imports a pre-configured logger for printing status messages.


class CVCamera(BaseCamera):
    def __init__(self, cam_index=0): #cam_index=0: It accepts a camera index, which is typically 0 for the default built-in webcam. If you have multiple cameras, you could use 1, 2, and so on.
        logging_default.info("Setting up the camera")
        self.cap = cv2.VideoCapture(cam_index) #calls cv2.VideoCapture() with the camera index to create a video capture object. This object is the connection to the physical camera hardware



    #Tuple is an ordered collection of lements but it is immutable (elements cannot be changed)
    def get_capture(self) -> np.ndarray: #capture a single frame from the camera
        ret, frame = self.cap.read() #Method call that returns a tuple 
        #ret is a Boolean that is True if frame was successfully read and Otherwise False
        #frame: is the actual image data as a NumPy array
        if ret and frame is not None:
            return True, frame
        logging_default.warning("cv2.VideoCapture returned None Frame!")
        return False, None

    def release(self):
        if self.cap: #Conditional check if the self.cap object exists to avoid errors if release is called on an uninitialized camera
            logging_default.info("Releasing camera device!")
            self.cap.release()
