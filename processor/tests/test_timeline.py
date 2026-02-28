from processor.timeline import render_timeline


def test_render_timeline_no_clips():
    """render_timeline should return an error when no clips are provided."""
    project = {"clips": [], "output_width": 1920, "output_height": 1080}
    result = render_timeline(project, {}, "/tmp/out.mp4")
    assert isinstance(result, str)
    assert result.startswith("error")


def test_render_timeline_missing_feeds():
    """render_timeline should error when feed paths are not provided."""
    project = {
        "clips": [{"feed_id": "cam1", "timeline_start": 0.0}],
        "output_width": 1920,
        "output_height": 1080,
    }
    result = render_timeline(project, {}, "/tmp/out.mp4")
    assert isinstance(result, str)
    assert result.startswith("error")


def test_render_timeline_handles_missing_ffmpeg():
    """render_timeline should return an error string when ffmpeg is unavailable."""
    project = {
        "clips": [
            {"feed_id": "cam1", "timeline_start": 0.0, "trim_start": None, "trim_end": None},
        ],
        "output_width": 1920,
        "output_height": 1080,
    }
    result = render_timeline(project, {"cam1": "/tmp/cam1.mp4"}, "/tmp/out.mp4")
    assert isinstance(result, str)
    assert result.startswith("error")


def test_render_timeline_with_trim_points():
    """render_timeline with trim points should return an error (ffmpeg missing), not crash."""
    project = {
        "clips": [
            {"feed_id": "cam1", "timeline_start": 0.0, "trim_start": 5.0, "trim_end": 30.0},
        ],
        "output_width": 1920,
        "output_height": 1080,
    }
    result = render_timeline(project, {"cam1": "/tmp/cam1.mp4"}, "/tmp/out.mp4")
    assert isinstance(result, str)
    assert result.startswith("error")
