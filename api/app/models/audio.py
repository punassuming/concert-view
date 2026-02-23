from pydantic import BaseModel


class AudioSyncRequest(BaseModel):
    feed_ids: list[str]


class AudioSyncResult(BaseModel):
    feed_id: str
    detected_offset_seconds: float
    confidence: float


class AudioOptimizeRequest(BaseModel):
    feed_ids: list[str]
    master_feed_id: str
    normalize: bool = True
    noise_reduce: bool = False


class AudioOptimizeResult(BaseModel):
    output_path: str
    settings_applied: dict
