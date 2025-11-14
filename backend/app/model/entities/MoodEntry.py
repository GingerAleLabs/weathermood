from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class MoodEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.now)
    mood: int
    note: Optional[str] = None
    temperature: float
    weather_rating: int #from WEATHER_SCALE
    