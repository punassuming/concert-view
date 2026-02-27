from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TimelineClip(BaseModel):
    """A single clip placed on the project timeline."""

    feed_id: str
    timeline_start: float = 0.0
    trim_start: Optional[float] = None
    trim_end: Optional[float] = None


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    clips: list[TimelineClip] = Field(default_factory=list)
    output_width: int = 1920
    output_height: int = 1080
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectCreate(BaseModel):
    name: str
    clips: list[TimelineClip] = Field(default_factory=list)
    output_width: Optional[int] = 1920
    output_height: Optional[int] = 1080


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    clips: Optional[list[TimelineClip]] = None
    output_width: Optional[int] = None
    output_height: Optional[int] = None
