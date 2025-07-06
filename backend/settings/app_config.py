import json

from pydantic import BaseModel

APP_CONFIG_PATH = "config/app_settings.json"

class PipelineSettings(BaseModel):
    drowsiness_model_run: bool
    phone_detection_model_run: bool
    hands_detection_model_run: bool
    inference_engine : str

class ConnectionStrings(BaseModel):
    db_connections: str

class ApiSettings(BaseModel):
    vehicle_id: str
    server: str
    device: str
    static_dir : str
    image_event_dir : str
    send_to_server: bool

class AppConfig(BaseModel):
    PipelineSettings: PipelineSettings
    ConnectionStrings: ConnectionStrings
    ApiSettings: ApiSettings

    @classmethod
    def load(cls, path: str = APP_CONFIG_PATH):
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

# Load the config once
settings = AppConfig.load()
