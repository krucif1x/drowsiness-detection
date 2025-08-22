from fastapi import APIRouter, HTTPException, status #Import FastAPI router, exception type, and HTTP status codes

from backend.domain.dto.base_response import StandardResponse #Standardized response schema for API responses
from backend.services.detection_background_service import DetectionBackgroundService # Service managing background detection thread


def detection_control_router(detection_service: DetectionBackgroundService) -> APIRouter:
    #Factory function that takes a DetectionBackgroundService instance and returns a configured APIrouter
    router = APIRouter()

    @router.post(
        "/start", #Endpoint path: POST /start
        description="Start the detection background thread.", # OpenAPI description
        response_model=StandardResponse # Responses will be serialized as StandardResponse
    )
    def start_detection():
        #Handler to start the background detection process
        try:
            status = detection_service.start() # Ask the service to start; returns status/info
            return StandardResponse(status="success", message="Detection started.", data=status) # Return success with data
        except Exception as e:
            # On any error, raise a 500 Internal Server Error with details
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start detection: {str(e)}"
            )
        
    @router.post(
        "/restart", # Endpoint path: POST /restart
        description="Re-Start the detection background thread.", # Description (note: typically 'Restart')
        response_model=StandardResponse
    )
    def restart_detection():
        # Handler to restart the background detection process
        try:
            status = detection_service.restart() # Restart operation on the service
            return StandardResponse(status="success", message="Detection started.", data=status) # Respond success
        except Exception as e:
            # On error, return 500 with message
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to start detection: {str(e)}"
            )

    @router.post(
        "/pause", # Endpoint path: POST /pause
        description="Pause the detection thread.", # Description
        response_model=StandardResponse
    )
    def pause_detection():
        # Handler to pause the background detection process
        try:
            status = detection_service.pause() # Pause operation; returns status/info
            return StandardResponse(status="success", message="Detection paused.", data=status) # Respond success
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to pause detection: {str(e)}"
            )

    @router.post(
        "/resume", # Endpoint path: POST /resume
        description="Resume the paused detection thread.",
        response_model=StandardResponse
    )
    def resume_detection():
        # Handler to resume a previously paused detection process
        try:
            status = detection_service.resume() # Resume operation; returns status/info
            return StandardResponse(status="success", message="Detection resumed.", data=status)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to resume detection: {str(e)}"
            )

    @router.post(
        "/stop", # Endpoint path: POST /stop
        description="Stop the detection thread.",
        response_model=StandardResponse
    )
    def stop_detection():
        # Handler to stop the background detection process
        try:
            status = detection_service.stop() # Stop operation; returns status/info
            return StandardResponse(status="success", message="Detection stopped.", data=status)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to stop detection: {str(e)}"
            )

    @router.get(
        "/status", # Endpoint path: GET /status
        description="Get the current detection status.",
        response_model=StandardResponse
    )
    def detection_status():
        # Handler to fetch the current status of the detection process
        try:
            is_alive_thread = detection_service.is_active()
            is_running = detection_service.is_running
            status_msg = "running" if is_alive_thread and is_running else "stopped or paused"
            
            return StandardResponse(
                status="success",
                message=f"Detection is {status_msg}.",
                data={
                    "is_alive": is_alive_thread,
                    "is_running": is_running
                }
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get detection status: {str(e)}"
            )

    return router
