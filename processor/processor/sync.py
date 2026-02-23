import subprocess
import logging

import numpy as np

logger = logging.getLogger(__name__)


def extract_audio_pcm(video_path: str, sample_rate: int = 16000) -> np.ndarray:
    """Extract audio from a video file as a numpy array of float32 PCM samples."""
    cmd = [
        "ffmpeg", "-i", video_path,
        "-vn", "-ac", "1",
        "-ar", str(sample_rate),
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "pipe:1",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, check=True,
        )
    except FileNotFoundError:
        logger.warning("ffmpeg not found; returning empty array")
        return np.array([], dtype=np.float32)
    except subprocess.CalledProcessError as exc:
        logger.error("ffmpeg failed: %s", exc.stderr.decode(errors="replace"))
        return np.array([], dtype=np.float32)

    samples = np.frombuffer(result.stdout, dtype=np.int16).astype(np.float32)
    # Normalize to [-1, 1]
    if samples.size > 0:
        samples /= 32768.0
    return samples


def detect_offset(reference_path: str, target_path: str) -> dict:
    """Detect the audio offset between a reference and target file.

    Uses cross-correlation of extracted PCM audio.
    Returns {"offset_seconds": float, "confidence": float}.
    """
    sample_rate = 16000
    ref = extract_audio_pcm(reference_path, sample_rate)
    tgt = extract_audio_pcm(target_path, sample_rate)

    if ref.size == 0 or tgt.size == 0:
        logger.warning("Could not extract audio; returning mock offset")
        return {"offset_seconds": 0.0, "confidence": 0.0}

    # Cross-correlation via numpy
    correlation = np.correlate(ref, tgt, mode="full")
    peak_index = int(np.argmax(np.abs(correlation)))
    offset_samples = peak_index - (len(tgt) - 1)
    offset_seconds = offset_samples / sample_rate

    peak_value = float(np.abs(correlation[peak_index]))
    norm = float(np.sqrt(np.sum(ref ** 2) * np.sum(tgt ** 2)))
    confidence = peak_value / norm if norm > 0 else 0.0

    return {"offset_seconds": round(offset_seconds, 4), "confidence": round(confidence, 4)}
