from fastapi import APIRouter, HTTPException 
#APIRouter is used to crate a modular group of API endpoints (routes) that can be inlcuded in the main FastAPI application
#HTTPException is used to raise HTTP errors with specific status codes and messages

from backend.domain.dto.base_response import StandardResponse
from backend.domain.dto.buzzer_dto import BeepRequest
from backend.services.buzzer_service import BuzzerService


#GET request is an HTTP request method used to retrive data or information from a server withoout altering any data on the server

def buzzer_router(buzzer_service: BuzzerService): #Creates and returns an APIRouter conifgured with buzzer-related endpoints
#Accepts a BuzzerService instance as an arguent
    router = APIRouter()

    @router.get( #Decorates the following function as a GET endpoint at the path/test realtive to wherever this router tis mounted
        "/test", 
        summary="Test a buzzer beep", 
        response_model=StandardResponse, #Tells FastAPI to validate/serialize the returned data into the StandardResponse schema
        description="""
        Quick test to check whether the buzzer is actually functional or not 
        """
    )
    async def trigger_beep_test(): #An asynchronous path operation function that will handle GET requests to /test
        try:
            buzzer_service.test_buzzer() #buzzer hardware is commanded to performa a quick test beep
            return StandardResponse( #serviec calls succeeds leads to a StandardResponse object made
                status="success", #FastAPI will serialize this Pydantic model to JSON
                message="Beeped"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Buzzer failed: {str(e)}")

    @router.post( #Decorates the next function as a POPST endpoint at /beep
        "/beep", 
        summary="Trigger a buzzer beep", 
        response_model=StandardResponse,
        description="""
        Triggers the buzzer to beep a specified number of times, each with a defined 
        duration, frequency, and pause interval between beeps.
        """
    )
    async def trigger_beep(req: BeepRequest): #async handler for POST/beep requests
        try:
            buzzer_service.beep_buzzer(req.times, req.duration, req.pause, req.frequency) #Decalres that the request body must be parsed and validated against the BeepRequest Pydantic model
            return StandardResponse(
                status="success",
                message=f"Beeped {req.times} time(s)."
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Buzzer failed: {str(e)}")

    return router
