from fastapi import APIRouter, HTTPException

from app.models.audio import (
    AudioOptimizeRequest,
    AudioOptimizeResult,
    AudioSyncRequest,
    AudioSyncResult,
)
from app.routers.feeds import _feeds
from app.services.audio_service import analyze_sync, optimize_audio

router = APIRouter(prefix="/api/audio", tags=["audio"])


@router.post("/sync")
async def sync_audio(body: AudioSyncRequest) -> list[AudioSyncResult]:
    feed_paths: list[str] = []
    for fid in body.feed_ids:
        feed = _feeds.get(fid)
        if not feed:
            raise HTTPException(status_code=404, detail=f"Feed {fid} not found")
        feed_paths.append(feed.file_path or feed.source_url)
    return await analyze_sync(feed_paths, body.feed_ids)


@router.post("/optimize")
async def optimize(body: AudioOptimizeRequest) -> AudioOptimizeResult:
    feed_paths: list[str] = []
    master_path: str = ""
    for fid in body.feed_ids:
        feed = _feeds.get(fid)
        if not feed:
            raise HTTPException(status_code=404, detail=f"Feed {fid} not found")
        path = feed.file_path or feed.source_url
        feed_paths.append(path)
        if fid == body.master_feed_id:
            master_path = path
    if not master_path:
        raise HTTPException(status_code=404, detail="Master feed not found")
    return await optimize_audio(
        feed_paths, master_path, body.normalize, body.noise_reduce
    )
