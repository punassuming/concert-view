import subprocess
import logging

logger = logging.getLogger(__name__)


def compose_videos(
    layout: dict, feed_paths: dict[str, str], output_path: str
) -> str:
    """Compose multiple video feeds into a single output based on a layout.

    Args:
        layout: Dict with "output_width", "output_height", and "slots" list.
                Each slot has feed_id, x, y, width, height (fractions 0-1).
        feed_paths: Mapping of feed_id to file path.
        output_path: Destination file path for the composed video.

    Returns:
        The output file path on success, or an error string.
    """
    out_w = layout.get("output_width", 1920)
    out_h = layout.get("output_height", 1080)
    slots = layout.get("slots", [])

    if not slots:
        return "error: no slots defined in layout"

    # Build ffmpeg inputs and filter_complex
    inputs: list[str] = []
    filters: list[str] = []
    overlay_chain = ""

    for idx, slot in enumerate(slots):
        feed_id = slot["feed_id"]
        path = feed_paths.get(feed_id)
        if not path:
            logger.warning("No file for feed_id=%s, skipping", feed_id)
            continue

        px = int(slot["x"] * out_w)
        py = int(slot["y"] * out_h)
        pw = int(slot["width"] * out_w)
        ph = int(slot["height"] * out_h)

        inputs.extend(["-i", path])
        filters.append(f"[{idx}:v]scale={pw}:{ph}[s{idx}]")

        if idx == 0:
            overlay_chain = f"color=s={out_w}x{out_h}:c=black[base];[base][s0]overlay={px}:{py}[tmp0]"
        else:
            prev = f"tmp{idx - 1}"
            cur = f"tmp{idx}"
            overlay_chain += f";[{prev}][s{idx}]overlay={px}:{py}[{cur}]"

    if not inputs:
        return "error: no valid feeds for layout"

    last_label = f"tmp{len(slots) - 1}"
    filter_complex = ";".join(filters) + ";" + overlay_chain
    # Map the final overlay output
    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + ["-filter_complex", filter_complex, "-map", f"[{last_label}]",
           "-c:v", "libx264", "-preset", "fast", output_path]
    )

    logger.info("Running compose command: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        logger.warning("ffmpeg not found")
        return "error: ffmpeg not available"
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.decode(errors="replace")
        logger.error("ffmpeg compose failed: %s", msg)
        return f"error: ffmpeg failed – {msg[:200]}"

    return output_path
