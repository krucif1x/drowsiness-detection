import threading
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from backend.infrastructure.migrate import run_migrations
from backend.services.buzzer_service import BuzzerService
from backend.services.detection_background_service import DetectionBackgroundService
from backend.services.drowsiness_event_service import DrowsinessEventService
from backend.settings.app_config import settings
from backend.infrastructure.session import init_db, engine

from backend.lib.socket_trigger import SocketTrigger
from backend.routers import config_router, detection_control_router, drowsiness_realtime_router, app_version, buzzer_router, drowsiness_event_router
from backend.services.drowsiness_detection_service import DrowsinessDetectionService
from backend.services.phone_detection_service import PhoneDetectionService
from backend.services.hand_detection_service import HandsDetectionService

from backend.tasks.detection_task import DetectionTask
from backend.utils.frame_buffer import FrameBuffer
from backend.utils.logging import logging_default

from backend.hardware.factory_hardware import (
    get_camera,
    get_buzzer
)

# Building Services and Hardware connection
logging_default.info("Building services and initiated hardwares")
socket_trigger = SocketTrigger(settings.ApiSettings)
camera = get_camera()
buzzer = get_buzzer()

# Apply Alembic migrations
run_migrations()

# Create a manual DB session and inject service
db_session = Session(engine)
drowsiness_event_service = DrowsinessEventService(db_session)

buzzer_service = BuzzerService(buzzer)
drowsiness_service = DrowsinessDetectionService(buzzer_service, socket_trigger, drowsiness_event_service)
phone_detection_service = PhoneDetectionService(socket_trigger)
hand_service = HandsDetectionService(socket_trigger)

detection_task = DetectionTask()

# Create shared frame buffer
frame_buffer = FrameBuffer()

detection_background_service = DetectionBackgroundService(
    detection_task,
    drowsiness_service,
    phone_detection_service,
    hand_service,
    camera,
    frame_buffer
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start detection loop thread that will run the drowsiness service on app startup
    # source = https://stackoverflow.com/questions/70872276/fastapi-python-how-to-run-a-thread-in-the-background 
    detection_background_service.start()
    yield

    # Event when shutdown the FastAPI
    camera.release()
    buzzer.cleanup()
    db_session.close()
    detection_background_service.stop()

# Define Fast API App
logging_default.info("Run webApp")
app = FastAPI(
    title="Drowsiness Detection System",
    description="This page contains detailed info of drowsiness detection system by Capability Center Division Program",
    lifespan=lifespan
)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static files for the image drowsiness event
os.makedirs(settings.ApiSettings.static_dir, exist_ok=True)
app.mount(f"/{settings.ApiSettings.static_dir}", StaticFiles(directory=f"{settings.ApiSettings.static_dir}"), name="static")

# Register router
logging_default.info("Registering API routers")
app.include_router(app_version.router, prefix="/version", tags=["Version"])
app.include_router(buzzer_router.buzzer_router(buzzer_service), prefix="/buzzer", tags=["Buzzer"])
app.include_router(config_router.config_router(drowsiness_service, phone_detection_service, detection_task), prefix="/config", tags=["config"])
app.include_router(detection_control_router.detection_control_router(detection_background_service), prefix="/detection", tags=["Detection Control"])
app.include_router(drowsiness_realtime_router.drowsiness_realtime_router(frame_buffer), prefix="/realtime", tags=["Realtime Drowsiness"])
app.include_router(drowsiness_event_router.router, prefix="/drowsinessevent", tags=["Drowsiness Event"])