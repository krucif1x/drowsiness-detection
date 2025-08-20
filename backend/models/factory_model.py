import os #Used to check the current operating system
#from back.setttings....: These lines import config classes
from backend.settings.detection_config import PhoneDetectionConfig
from backend.settings.model_config import FaceMeshConfig, HandsConfig

hailo_inference_engine = None #Variable that is set to None, acts as a Flag
if os.name == "posix": #It checks if the operating system is "posix," which is the name for Unix-like systems such as Linux
    try: # Attempts to import the HailoInferenceEngine library and create an instance of it
        from backend.models.hailo.hailo_runtime.hailo_inference_engine import (
            HailoInferenceEngine,
        )
        hailo_inference_engine = HailoInferenceEngine()
    except ImportError:
        hailo_inference_engine = None


def get_face_model(config : FaceMeshConfig, inference_engine : str): #Takes a config object adn an inference_engine string to decide which face model to load
    if os.name == "nt": #f the code is running on Windows, it immediately imports and returns the standard MediapipeFaceMeshModel
        from backend.models.mediapipe_wrappers.mediapipe_face_model import (
            MediapipeFaceMeshModel,
        )
        return MediapipeFaceMeshModel(config)
    try: #Main selection logic for non-Windows systems
    """    
    Function:

1. It first checks if the user explicitly requested the "hailo" engine. If so, it tries to import and return the hardware-accelerated BlazeFacePipeline.

2. If the engine is not "hailo" or if the if condition is passed, it falls back to importing and returning the standard MediapipeFaceMeshModel.

3. If any error occurs during this process (e.g., the Hailo library is missing), the except block catches it and returns the safe MediapipeFaceMeshModel as a final fallback.
     """  
        if inference_engine == "hailo":
            from backend.models.hailo.blaze_model.face_mesh.blaze_face_pipeline import (
                BlazeFacePipeline,
            )
            return BlazeFacePipeline(hailo_inference_engine)
        
        from backend.models.mediapipe_wrappers.mediapipe_face_model import (
            MediapipeFaceMeshModel,
        )
        return MediapipeFaceMeshModel(config)
    
    except ImportError or NotImplementedError:
        from backend.models.mediapipe_wrappers.mediapipe_face_model import (
            MediapipeFaceMeshModel,
        )
        return MediapipeFaceMeshModel(config)

def get_body_pose_model(config : PhoneDetectionConfig, inference_engine : str): #currently only returns the MediaPipe model. The # TODO comment indicates that a Hailo-accelerated version is planned but has not been implemented yet.
    if os.name == "nt":
        from backend.models.mediapipe_wrappers.mediapipe_body_model import (
            MediapipeBodyPoseModel,
        )
        return MediapipeBodyPoseModel(config)
    try:
        # TODO : Implement Body Pose Model run for Hailo Acceleration
        from backend.models.mediapipe_wrappers.mediapipe_body_model import (
            MediapipeBodyPoseModel,
        )
        return MediapipeBodyPoseModel(config)
    
    except ImportError or NotImplementedError:
        from backend.models.mediapipe_wrappers.mediapipe_body_model import (
            MediapipeBodyPoseModel,
        )
        return MediapipeBodyPoseModel(config)
        
def get_hands_pose_model(config : HandsConfig, inference_engine : str): #follows the exact same logic as get_face_model, providing either a Hailo-accelerated hand tracking model or the standard MediaPipe version as a fallback.
    if os.name == "nt":
        from backend.models.mediapipe_wrappers.mediapipe_hands_model import (
            MediapipeHandsModel,
        )
        return MediapipeHandsModel(config)
    try:
        if inference_engine == "hailo":
            from backend.models.hailo.blaze_model.hands.blaze_hands_pipeline import (
                BlazeHandsPipeline,
            )
            return BlazeHandsPipeline(hailo_inference_engine)

        from backend.models.mediapipe_wrappers.mediapipe_hands_model import (
            MediapipeHandsModel,
        )
        return MediapipeHandsModel(config)
    
    except ImportError or NotImplementedError:
        from backend.models.mediapipe_wrappers.mediapipe_hands_model import (
            MediapipeHandsModel,
        )
        return MediapipeHandsModel(config)
        
