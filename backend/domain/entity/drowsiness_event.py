from datetime import datetime #Library for dates and times, specifically for the timestamp field
from uuid import UUID # An Universally Unique Identifier and used to make uniwue ID for each event record

from sqlmodel import Column, Field, SQLModel, String # Core components from the sqlmodel library
from uuid6 import uuid7 #This is a function from the uuid6 library that generates a special kind of UUID (Version 7)


class DrowsinessEvent(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    vehicle_identification: str = Field(..., sa_column=Column(String, nullable=False))
    timestamp: datetime = Field(default_factory=datetime.now)
    image: str = Field(..., sa_column=Column(String, nullable=False))
    ear: float
    mar: float
    event_type: str = Field(..., sa_column=Column(String, nullable=False))
