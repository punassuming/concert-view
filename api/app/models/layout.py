from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class LayoutSlot(BaseModel):
    feed_id: str
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    width: float = Field(ge=0.0, le=1.0)
    height: float = Field(ge=0.0, le=1.0)
    z_index: int = 0


class Layout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    slots: list[LayoutSlot]
    output_width: int = 1920
    output_height: int = 1080
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class LayoutCreate(BaseModel):
    name: str
    slots: list[LayoutSlot]
    output_width: Optional[int] = 1920
    output_height: Optional[int] = 1080


class LayoutUpdate(BaseModel):
    name: Optional[str] = None
    slots: Optional[list[LayoutSlot]] = None


class LayoutSuggestionRequest(BaseModel):
    feed_count: int
    style: str = "grid"


class LayoutSuggestionResponse(BaseModel):
    layout: Layout
    description: str
