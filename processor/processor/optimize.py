import subprocess
import logging

logger = logging.getLogger(__name__)


def normalize_audio(input_path: str, output_path: str) -> str:
    """Normalize audio levels using the ffmpeg loudnorm filter.

    Returns the output path on success or an error string.
    """
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        output_path,
    ]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        logger.warning("ffmpeg not found")
        return "error: ffmpeg not available"
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.decode(errors="replace")
        logger.error("normalize_audio failed: %s", msg)
        return f"error: {msg[:200]}"
    return output_path


def reduce_noise(input_path: str, output_path: str) -> str:
    """Basic noise reduction using the ffmpeg afftdn filter.

    Returns the output path on success or an error string.
    """
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-af", "afftdn=nf=-25",
        output_path,
    ]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        logger.warning("ffmpeg not found")
        return "error: ffmpeg not available"
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.decode(errors="replace")
        logger.error("reduce_noise failed: %s", msg)
        return f"error: {msg[:200]}"
    return output_path


def optimize_audio(
    input_path: str,
    output_path: str,
    normalize: bool = True,
    noise_reduce: bool = False,
) -> dict:
    """Apply selected audio optimizations.

    Returns a dict with the settings applied and the result path or error.
    """
    settings: dict = {
        "normalize": normalize,
        "noise_reduce": noise_reduce,
    }

    current = input_path

    if normalize:
        norm_out = output_path if not noise_reduce else output_path + ".norm.tmp"
        result = normalize_audio(current, norm_out)
        if result.startswith("error"):
            return {**settings, "result": result}
        current = result

    if noise_reduce:
        result = reduce_noise(current, output_path)
        if result.startswith("error"):
            return {**settings, "result": result}
        current = result

    if not normalize and not noise_reduce:
        current = input_path

    return {**settings, "result": current}
