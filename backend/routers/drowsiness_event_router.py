from typing import List # For type annotations like List [DrowsinessEvent]

from fastapi import APIRouter, Depends, HTTPException, status # FastAPI routing, DI, and HTTP utilities
from fastapi.responses import FileResponse # To return files (e.g., images) as HTTP responses

from backend.domain.dto.base_response import StandardResponse
from backend.domain.entity.drowsiness_event import DrowsinessEvent
from backend.services.dependencies import get_drowsiness_event_service
from backend.services.drowsiness_event_service import DrowsinessEventService

router = APIRouter() # Create a router to register endpoints for drowsiness events

@router.get(
    "/", # Route: GET / (under whatever prefix you mount this router)
    description="Retrieve all drowsiness events, sorted by timestamp.",
    response_model=List[DrowsinessEvent] # FastAPI will serialize list of events using this model
    )
def list_events(service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
    # Endpoint to list all events; service is injected via Depends
    try:
        events = service.get_all_events()  # Assuming the service method is async
        return events
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the events: {str(e)}"
        )
    
@router.get(
    "/{event_id}", # Route: GET /{event_id} to fetch a single event by ID
    description="Retrieve a drowsiness event by ID.",
    response_model=DrowsinessEvent # Response is a single event model
)
def get_event(event_id: str, service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
    # Endpoint to fetch a single event by its ID
    try:
        event = service.get_event_by_id(event_id) # Lookup by ID
        if event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drowsiness event not found"
            )
        return event
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the event: {str(e)}"
        )

@router.get(
    "/download/{event_id}", # Route: GET /download/{event_id}
    description="Download the drowsiness event by Event ID",
    response_model=StandardResponse # Note: FileResponse bypasses model; response_model here is mostly for docs and may be misleading
)
async def download_image_event(event_id : str, service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
    # Endpoint to download an event's image/file by ID
    try:
        # Service returns a tuple with file path, MIME type, and a suggested filename
        file_path, content_type, file_name = service.download_event_image(event_id)
        headers = {'Access-Control-Expose-Headers': 'Content-Disposition'}

        # Return the file as a streaming response with correct headers and filename
        return FileResponse(
            path=file_path,
            media_type=content_type,
            filename=file_name,
            headers=headers
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the event: {str(e)}"
        )

@router.post(
    "/", # Route: POST / to create a new event
    description="Create a new drowsiness event.",
    response_model=DrowsinessEvent # Return the created event
)
def create_event(event: DrowsinessEvent, service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
    # Endpoint to create a new event; request body validated as DrowsinessEvent
    try:
        # Creating the event via the service
        created_event = service.create_event(event)
        return created_event
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the event: {str(e)}"
        )

@router.delete(
    "/{event_id}", # Route: DELETE /{event_id} to delete an event by ID
    description="Delete a drowsiness event by ID.",
    response_model=dict # Returns a simple message dict on success
)
def delete_event(event_id: str, service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
    # Endpoint to delete an event
    try:
        success = service.delete_event(event_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drowsiness event not found"
            )
        return {"message": "Drowsiness event deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the event: {str(e)}"
        )
