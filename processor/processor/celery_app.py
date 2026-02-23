import os
import logging

from celery import Celery

logger = logging.getLogger(__name__)

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app = Celery("processor", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@app.task
def detect_offset_task(reference_path: str, target_path: str) -> dict:
    """Celery task: detect audio offset between two video files."""
    from processor.sync import detect_offset

    logger.info("Running detect_offset_task: ref=%s target=%s", reference_path, target_path)
    return detect_offset(reference_path, target_path)


@app.task
def compose_videos_task(layout: dict, feed_paths: dict, output_path: str) -> str:
    """Celery task: compose multiple video feeds into a single output file."""
    from processor.compose import compose_videos

    logger.info("Running compose_videos_task: output=%s", output_path)
    return compose_videos(layout, feed_paths, output_path)


@app.task
def optimize_audio_task(
    input_path: str,
    output_path: str,
    normalize: bool = True,
    noise_reduce: bool = False,
) -> dict:
    """Celery task: apply audio optimizations to a file."""
    from processor.optimize import optimize_audio

    logger.info("Running optimize_audio_task: input=%s output=%s", input_path, output_path)
    return optimize_audio(input_path, output_path, normalize, noise_reduce)
