import asyncio # For async utilities like sleep and running blocking code in threads

from fastapi import APIRouter, WebSocket, WebSocketDisconnect # FastAPI router and WebSocket types
from fastapi.responses import StreamingResponse # For streaming HTTP responses (e.g., MJPEG video)


from backend.streaming.drowsiness_streaming import (
    stream_debug_camera_feed, # Generator that yields debug MJPEG frames
    stream_processed_drowsiness_feed,# Generator that yields processed (annotated) MJPEG frames
    stream_raw_camera_feed,# Generator that yields raw MJPEG frames
)
from backend.utils.frame_buffer import FrameBuffer # Shared buffer providing frames/metrics between producer and API
from backend.utils.logging import logging_default # App-wide logger


def drowsiness_realtime_router(frame_buffer : FrameBuffer):
    # Factory that receives a FrameBuffer dependency and returns a configured APIRouter
    router = APIRouter() # Create router to register HTTP and WebSocket endpoints

    @router.get(
        "/video/raw", # HTTP route serving the raw camera stream
        summary="Live un-edit and raw data of video feed from the camera",
        description="Returns a live video stream (MJPEG). Use a browser instead of Swagger to view."
    )
    def video_feed():
        # Returns a streaming MJPEG response from the raw camera feed
        return StreamingResponse(
            stream_raw_camera_feed(frame_buffer),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )

    @router.get(
        "/video/processed", # HTTP route serving the processed (annotated) stream
        summary="Live of processed detection result frame of video feed from the camera",
        description="Returns a live video stream (MJPEG). Use a browser instead of Swagger to view."
    )
    def video_drowsiness_feed():
        # Returns a streaming MJPEG response from the processed drowsiness feed
        return StreamingResponse(
            stream_processed_drowsiness_feed(frame_buffer), # Generator for annotated frames (e.g., boxes/labels)
            media_type="multipart/x-mixed-replace; boundary=frame" # MJPEG content type
        )
    
    @router.get(
        "/video/debug", # HTTP route serving a debug view of frames
        summary="Live of debug one of detection result frame of video feed from the camera",
        description="Returns a live video stream (MJPEG). Use a browser instead of Swagger to view."
    )
    def video_debug_feed():
        # Returns a streaming MJPEG response for debugging frames
        return StreamingResponse(
            stream_debug_camera_feed(frame_buffer), # Generator for debug frames
            media_type="multipart/x-mixed-replace; boundary=frame" # MJPEG content type
        )
     
    @router.websocket("/data/facialmetrics") # WebSocket route streaming facial metric data in realtime
    async def stream_facial_metrics_data(websocket: WebSocket):
        await websocket.accept() # Accept the WebSocket handshake
        logging_default.info("A client has been connected to WebSocket Facial Metrics")
        try:
            while True:
                # Run the get_facial_metrics function in a non-blocking manner
                facial_metrics = await asyncio.to_thread(frame_buffer.get_facial_metrics)

                if facial_metrics: # Continuous push loop
                    # Send the facial metrics as JSON if available
                    await websocket.send_json(facial_metrics.model_dump())
                else:
                    # Default values if no metrics are available
                    await websocket.send_json({"ear": 0.0, "mar": 0.0, "is_drowsy" : False, "is_calling" : "false"})

                # Hack for now
                # Small delay to prevent busy loop and potential client overload
                await asyncio.sleep(0.01)

        except WebSocketDisconnect:
            # Client disconnected gracefully; log and exit handler
            logging_default.info("A client has been disconnected from WebSocket Facial Metrics")
    
    @router.websocket("/notification/drowsiness") # WebSocket route pushing recent drowsiness/yawning events
    async def stream_recent_drowsiness_data(websocket: WebSocket):
        await websocket.accept() # Accept WebSocket connection
        logging_default.info("A client has been connected to WebSocket Drowsiness Recent Event")
        try:
            while True:
                # Run to get the recent drowsiness event happen in a non-blocking manner
                drowsiness_event_metrics = await asyncio.to_thread(frame_buffer.get_drowsiness_event_recent)
                if (drowsiness_event_metrics.drowsiness_event):
                    await websocket.send_json(drowsiness_event_metrics.drowsiness_event)
                if (drowsiness_event_metrics.yawning_event):
                    await websocket.send_json(drowsiness_event_metrics.yawning_event)

                # Hack for now : Reset the frame
                # If I add sleep instead, there is no guarantee that the timing that I set will match, if
                # set them to slow, it risk I don't get the latest data
                # if to fast, I just get another duplicate data
                await asyncio.to_thread(frame_buffer.update_drowsiness_event_recent, None, None)

        except WebSocketDisconnect:
            logging_default.info("A client has been disconnected from WebSocket Drowsiness Recent Event")


    return router
