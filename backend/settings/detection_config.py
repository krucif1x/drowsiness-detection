import json

from pydantic import BaseModel

DETECTION_CONFIG_PATH = "config/detection_settings.json"

class DrowsinessConfig(BaseModel):
    eye_aspect_ratio_threshold: float
    eye_aspect_ratio_consec_frames: int
    mouth_aspect_ratio_threshold: float
    mouth_aspect_ratio_consec_frames: int
    apply_masking: bool

class PhoneDetectionConfig(BaseModel):
    distance_threshold: int

class DetectionConfig(BaseModel):
    drowsiness: DrowsinessConfig
    phone_detection: PhoneDetectionConfig

    @classmethod
    def load(cls, path: str = DETECTION_CONFIG_PATH):
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    def save(self, path: str = DETECTION_CONFIG_PATH):
        with open(path, "w") as f:
            json.dump(self.model_dump(), f, indent=2)
    
# Load the config once
detection_settings = DetectionConfig.load()