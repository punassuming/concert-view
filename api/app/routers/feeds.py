from fastapi import APIRouter, HTTPException, UploadFile

from app.config import settings
from app.models.feed import Feed, FeedCreate, FeedUpdate
from app.services.feed_service import save_upload

router = APIRouter(prefix="/api/feeds", tags=["feeds"])

_feeds: dict[str, Feed] = {}


@router.get("/")
async def list_feeds() -> list[Feed]:
    return list(_feeds.values())


@router.post("/", status_code=201)
async def create_feed(body: FeedCreate) -> Feed:
    feed = Feed(name=body.name, source_url=body.source_url)
    _feeds[feed.id] = feed
    return feed


@router.get("/{feed_id}")
async def get_feed(feed_id: str) -> Feed:
    feed = _feeds.get(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    return feed


@router.patch("/{feed_id}")
async def update_feed(feed_id: str, body: FeedUpdate) -> Feed:
    feed = _feeds.get(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    update_data = body.model_dump(exclude_unset=True)
    updated = feed.model_copy(update=update_data)
    _feeds[feed_id] = updated
    return updated


@router.delete("/{feed_id}", status_code=204)
async def delete_feed(feed_id: str):
    if feed_id not in _feeds:
        raise HTTPException(status_code=404, detail="Feed not found")
    del _feeds[feed_id]
    return None


@router.post("/{feed_id}/upload")
async def upload_video(feed_id: str, file: UploadFile):
    feed = _feeds.get(feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="Feed not found")
    file_path = await save_upload(feed_id, file, settings.UPLOAD_DIR)
    updated = feed.model_copy(update={"file_path": file_path})
    _feeds[feed_id] = updated
    return {"file_path": file_path}
