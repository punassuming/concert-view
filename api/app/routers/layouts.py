from fastapi import APIRouter, HTTPException

from app.config import settings
from app.models.layout import (
    Layout,
    LayoutCreate,
    LayoutSuggestionRequest,
    LayoutSuggestionResponse,
    LayoutUpdate,
)
from app.services.ai_service import get_layout_suggestion

router = APIRouter(prefix="/api/layouts", tags=["layouts"])

_layouts: dict[str, Layout] = {}


@router.get("/")
async def list_layouts() -> list[Layout]:
    return list(_layouts.values())


@router.post("/", status_code=201)
async def create_layout(body: LayoutCreate) -> Layout:
    layout = Layout(
        name=body.name,
        slots=body.slots,
        output_width=body.output_width or 1920,
        output_height=body.output_height or 1080,
    )
    _layouts[layout.id] = layout
    return layout


@router.get("/{layout_id}")
async def get_layout(layout_id: str) -> Layout:
    layout = _layouts.get(layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    return layout


@router.patch("/{layout_id}")
async def update_layout(layout_id: str, body: LayoutUpdate) -> Layout:
    layout = _layouts.get(layout_id)
    if not layout:
        raise HTTPException(status_code=404, detail="Layout not found")
    update_data = body.model_dump(exclude_unset=True)
    updated = layout.model_copy(update=update_data)
    _layouts[layout_id] = updated
    return updated


@router.delete("/{layout_id}", status_code=204)
async def delete_layout(layout_id: str):
    if layout_id not in _layouts:
        raise HTTPException(status_code=404, detail="Layout not found")
    del _layouts[layout_id]
    return None


@router.post("/suggest")
async def suggest_layout(body: LayoutSuggestionRequest) -> LayoutSuggestionResponse:
    return await get_layout_suggestion(
        body,
        openai_key=settings.OPENAI_API_KEY,
        gemini_key=settings.GEMINI_API_KEY,
    )
