import json #Read/Write config to JSON files

from fastapi import APIRouter, HTTPException # FastAPI routing and HTTP error handling
from pydantic import ValidationError #Catching Pydantic validation errors

from backend.domain.dto.base_response import StandardResponse
from backend.services.drowsiness_detection_service import DrowsinessDetectionService
from backend.services.phone_detection_service import PhoneDetectionService
from backend.settings.app_config import (
    APP_CONFIG_PATH, #File path to app's main config JSON
    PipelineSettings, #Pydantic model for pipeline settings structure/validation
    settings, #App-wide settings holder (likely a singleton/config object)
)
from backend.settings.detection_config import DetectionConfig, detection_settings
from backend.tasks.detection_task import DetectionTask


def config_router(
    drowsiness_service: DrowsinessDetectionService,
    phone_detection_service: PhoneDetectionService,
    detection_task : DetectionTask
):
    router = APIRouter() # Create a new APIRouter to register endpoints on

    @router.get(
        "/detection", # Routh path
        summary="Get current detection settings", #OpenAPI summary
        response_model=DetectionConfig, #FastAPI will serialize/validate the response as DetectionConfig
        description="""
        Retrieves the current configuration for both drowsiness and phone detection settings.
        """ #OpenAPI description
    )
    async def get_detection_config():
        try:
            return detection_settings #Retyurn the in-memorysingleton holding detectio configuration
        except Exception as e:
            #If anything unexpected happens, return HTTP 500 with error detail
            raise HTTPException(status_code=500, detail=f"Failed to fetch config: {str(e)}")

    @router.post(
        "/detection/update", #Routh Path
        summary="Update detection settings", # OpenAPI summary
        response_model=StandardResponse, #Responses will follow the StandardResponse schema
        description="""
        Updates and applies the detection configuration. This includes both drowsiness and phone detection settings. 
        After updating the in-memory settings and saving to the JSON config file, the related detection services are reinitialized.
        """
    )
    async def update_detection_config(req: DetectionConfig):
        try:
            # Update in-memory settings wiht incoming request values
            detection_settings.drowsiness = req.drowsiness
            detection_settings.phone_detection = req.phone_detection

            # Save the updated settings to disk (implmentation side DetectionConfig.save())
            detection_settings.save()

            # Reinitialize live servcies so changes take effect immediately
            drowsiness_service.drowsiness_detector.reinitialize_configuration(
                detection_settings.drowsiness #Pass new drowsines config
            )
            phone_detection_service.phone_detection.reinitialize_configuration(
                detection_settings.phone_detection # Pass new phone detection config
            )

            #Return a standardized success response
            return StandardResponse(
                status="success",
                message="Updated and applied detection config"
            )

        except ValidationError as ve:
            # If Pydantic validation fails, return 422 Unprocessable Entity with details
            raise HTTPException(status_code=422, detail=str(ve))
            # Any other unexpected error -> 500 Internal Server Error
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

    @router.get("/pipeline", response_model=PipelineSettings) # GET route returning current pipeline settings
    async def get_app_config():
        """Returns the entire config of App Settings.""" ## Docstring for OpenAPI/docs
        return settings.PipelineSettings# Return current in-memory pipeline settings
    
    @router.post("/pipeline/update",
        summary="Update pipeline settings", # OpenAPI summary
        response_model=StandardResponse, # Standardized response schema
        description="Updates and applies the pipeline configuration in runtime and file."
    )
    async def update_pipeline_settings(pipeline_data: PipelineSettings): ## Incoming payload validated as PipelineSettings
        try:
            # Update in-memory settings so the app immediately sees new pipeline values
            settings.PipelineSettings = pipeline_data

            # Open the JSON config file to persist pipeline settings to disk
            with open(APP_CONFIG_PATH, "r+") as f:
                data = json.load(f)
                data["PipelineSettings"] = pipeline_data.model_dump()
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            
             # Reinitialize the running detection task/pipeline to pick up new settings immediately
            detection_task.reinitialize_configuration()

            # Return standardized success response with a boolean data payload
            return StandardResponse(
                status="success",
                message="Pipeline settings updated and applied",
                data=True
            )
        except ValidationError as ve:
            raise HTTPException(status_code=422, detail=ve.errors())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
        
    return router
