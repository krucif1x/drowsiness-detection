from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from backend.domain.dto.base_response import StandardResponse
from backend.services.drowsiness_detection_service import DrowsinessDetectionService
from backend.services.phone_detection_service import PhoneDetectionService
from backend.settings.detection_config import DetectionConfig, detection_settings


def config_router(
    drowsiness_service: DrowsinessDetectionService,
    phone_detection_service: PhoneDetectionService
):
    router = APIRouter()

    @router.get(
        "/detection",
        summary="Get current detection settings",
        response_model=DetectionConfig,
        description="""
        Retrieves the current configuration for both drowsiness and phone detection settings.
        """
    )
    async def get_detection_config():
        try:
            return detection_settings
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch config: {str(e)}")

    @router.post(
        "/detection",
        summary="Update detection settings",
        response_model=StandardResponse,
        description="""
        Updates and applies the detection configuration. This includes both drowsiness and phone detection settings. 
        After updating the in-memory settings and saving to the JSON config file, the related detection services are reinitialized.
        """
    )
    async def update_detection_config(req: DetectionConfig):
        try:
            # Update in-memory settings
            detection_settings.drowsiness = req.drowsiness
            detection_settings.phone_detection = req.phone_detection

            # Save to disk
            detection_settings.save()

            # Apply new settings to live services
            drowsiness_service.drowsiness_detector.reinitialize_configuration(
                detection_settings.drowsiness
            )
            phone_detection_service.phone_detection.reinitialize_configuration(
                detection_settings.phone_detection
            )

            return StandardResponse(
                status="success",
                message="Updated and applied detection config"
            )

        except ValidationError as ve:
            raise HTTPException(status_code=422, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    return router