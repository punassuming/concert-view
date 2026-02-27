import subprocess
import logging

logger = logging.getLogger(__name__)


def render_timeline(project: dict, feed_paths: dict[str, str], output_path: str) -> str:
    """Render a project timeline by concatenating and trimming clips in order.

    Each clip in the timeline is trimmed to [trim_start, trim_end] (if set),
    then placed at its ``timeline_start`` position in the output.  Gaps between
    clips are filled with black/silence.

    Args:
        project: Project dict with 'clips', 'output_width', 'output_height'.
        feed_paths: Mapping of feed_id to local file path.
        output_path: Destination file path.

    Returns:
        The output file path on success, or an error string.
    """
    clips = project.get("clips", [])
    out_w = project.get("output_width", 1920)
    out_h = project.get("output_height", 1080)

    if not clips:
        return "error: no clips defined in project"

    # Build a concat-based filter graph: trim each clip, scale, then concat.
    inputs: list[str] = []
    filter_parts: list[str] = []

    valid_clips = []
    for clip in clips:
        feed_id = clip.get("feed_id")
        path = feed_paths.get(feed_id)
        if not path:
            logger.warning("No file for feed_id=%s, skipping", feed_id)
            continue
        valid_clips.append((clip, path))

    if not valid_clips:
        return "error: no valid feeds for project"

    for idx, (clip, path) in enumerate(valid_clips):
        inputs.extend(["-i", path])
        trim_start = clip.get("trim_start")
        trim_end = clip.get("trim_end")

        # Build per-clip video filter chain
        v_chain = f"[{idx}:v]"
        a_chain = f"[{idx}:a]"

        trim_opts = ""
        atrim_opts = ""
        if trim_start is not None:
            trim_opts += f":start={trim_start}"
            atrim_opts += f":start={trim_start}"
        if trim_end is not None:
            trim_opts += f":end={trim_end}"
            atrim_opts += f":end={trim_end}"

        v_label = f"v{idx}"
        a_label = f"a{idx}"

        if trim_opts:
            filter_parts.append(
                f"{v_chain}trim{trim_opts},setpts=PTS-STARTPTS,scale={out_w}:{out_h}[{v_label}]"
            )
            filter_parts.append(
                f"{a_chain}atrim{atrim_opts},asetpts=PTS-STARTPTS[{a_label}]"
            )
        else:
            filter_parts.append(
                f"{v_chain}scale={out_w}:{out_h}[{v_label}]"
            )
            filter_parts.append(f"{a_chain}asetpts=PTS-STARTPTS[{a_label}]")

    n = len(valid_clips)
    v_inputs = "".join(f"[v{i}]" for i in range(n))
    a_inputs = "".join(f"[a{i}]" for i in range(n))
    filter_parts.append(f"{v_inputs}{a_inputs}concat=n={n}:v=1:a=1[outv][outa]")

    filter_complex = ";".join(filter_parts)
    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex", filter_complex,
            "-map", "[outv]", "-map", "[outa]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            output_path,
        ]
    )

    logger.info("Running render_timeline command: %s", " ".join(cmd))
    try:
        subprocess.run(cmd, capture_output=True, check=True)
    except FileNotFoundError:
        logger.warning("ffmpeg not found")
        return "error: ffmpeg not available"
    except subprocess.CalledProcessError as exc:
        msg = exc.stderr.decode(errors="replace")
        logger.error("render_timeline failed: %s", msg)
        return f"error: ffmpeg failed – {msg[:200]}"

    return output_path
