import os

from fastapi import APIRouter
from celery.result import AsyncResult
from pydantic import BaseModel, Field

from app.celery_app import celery_app
from app.config import settings

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


class ComposeJobRequest(BaseModel):
    layout: dict = Field(
        ...,
        description=(
            "Layout definition with 'output_width', 'output_height', and 'slots' list. "
            "Each slot has feed_id, x, y, width, height (fractions 0-1)."
        ),
    )
    feed_paths: dict[str, str]
    output_filename: str


class SyncJobRequest(BaseModel):
    reference_path: str
    target_path: str


class OptimizeJobRequest(BaseModel):
    input_path: str
    output_filename: str
    normalize: bool = True
    noise_reduce: bool = False


@router.post("/compose", status_code=202)
async def dispatch_compose(body: ComposeJobRequest) -> dict:
    """Dispatch a video composition job to the Celery worker."""
    output_path = os.path.join(settings.OUTPUT_DIR, body.output_filename)
    task = celery_app.send_task(
        "processor.celery_app.compose_videos_task",
        args=[body.layout, body.feed_paths, output_path],
    )
    return {"job_id": task.id, "state": "PENDING"}


@router.post("/sync", status_code=202)
async def dispatch_sync(body: SyncJobRequest) -> dict:
    """Dispatch an audio-sync detection job to the Celery worker."""
    task = celery_app.send_task(
        "processor.celery_app.detect_offset_task",
        args=[body.reference_path, body.target_path],
    )
    return {"job_id": task.id, "state": "PENDING"}


@router.post("/optimize", status_code=202)
async def dispatch_optimize(body: OptimizeJobRequest) -> dict:
    """Dispatch an audio-optimization job to the Celery worker."""
    output_path = os.path.join(settings.OUTPUT_DIR, body.output_filename)
    task = celery_app.send_task(
        "processor.celery_app.optimize_audio_task",
        args=[body.input_path, output_path, body.normalize, body.noise_reduce],
    )
    return {"job_id": task.id, "state": "PENDING"}


@router.get("/{job_id}")
async def get_job_status(job_id: str) -> dict:
    """Return the current state (and result) of a Celery task."""
    result = AsyncResult(job_id, app=celery_app)
    response: dict = {"job_id": job_id, "state": result.state}
    if result.ready():
        if result.successful():
            response["result"] = result.result
        else:
            response["error"] = str(result.result)
    return response
