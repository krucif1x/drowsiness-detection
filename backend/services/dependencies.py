from fastapi import Depends
from sqlmodel import Session

from backend.infrastructure.session import get_session
from backend.services.drowsiness_event_service import DrowsinessEventService


def get_drowsiness_event_service(
    session: Session = Depends(get_session),
) -> DrowsinessEventService:
    """
    FastAPI dependency provider for DrowsinessEventService.

    - Uses `Depends(get_session)` to inject a database Session that is
      created/managed by your `get_session` dependency (often a context-managed
      session with proper commit/rollback/close behavior).
    - Returns a service instance bound to that session, which can be injected
      into route handlers.

    Usage in a FastAPI route:

        @router.get("/events")
        def list_events(service: DrowsinessEventService = Depends(get_drowsiness_event_service)):
            return service.list_events()

    This keeps route handlers thin and testable, and centralizes session handling.
    """
    # Construct the service with the injected SQLModel Session.
    # The service is typically responsible for all data access related to drowsiness events.
    return DrowsinessEventService(session)
