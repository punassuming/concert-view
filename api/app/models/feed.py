from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Feed(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    source_url: str
    file_path: Optional[str] = None
    duration_seconds: Optional[float] = None
    offset_seconds: float = 0.0
    volume: float = 1.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FeedCreate(BaseModel):
    name: str
    source_url: str


class FeedUpdate(BaseModel):
    name: Optional[str] = None
    offset_seconds: Optional[float] = None
    volume: Optional[float] = None
