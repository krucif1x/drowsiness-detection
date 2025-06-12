from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class PhoneState:
    is_calling: bool = False
    distance: Optional[float] = None
    timestamp: Optional[datetime] = datetime.now()
    body_landmark: Optional[Any] = None

@dataclass
class PhoneDetectionResult:
    detection: List[PhoneState] = field(default_factory=list)