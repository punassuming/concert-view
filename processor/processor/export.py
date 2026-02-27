import subprocess
import logging

logger = logging.getLogger(__name__)


def export_for_social(
    input_path: str,
    output_path: str,
    width: int,
    height: int,
) -> str:
    """Re-encode a video to the requested dimensions, padding as needed.

    Scales the video to fit within the target dimensions while preserving
    aspect ratio, then pads with black to reach the exact target size.
    Returns the output path on success or an error string.
    """
    scale_filter = (
        f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"
    )
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", scale_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        output_path,
    ]
    logger.info("Running export command: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        logger.warning("ffmpeg not found")
        return "error: ffmpeg not available"
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.decode(errors="replace")
        logger.error("export_for_social failed: %s", msg)
        return f"error: ffmpeg failed – {msg[:200]}"
    return output_path
