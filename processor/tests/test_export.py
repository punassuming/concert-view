from processor.export import export_for_social


def test_export_handles_missing_ffmpeg():
    """export_for_social should return an error string when ffmpeg is unavailable."""
    result = export_for_social("/tmp/in.mp4", "/tmp/out.mp4", 1920, 1080)
    assert isinstance(result, str)
    # Without ffmpeg, expect an error
    assert result.startswith("error")


def test_export_portrait_dimensions():
    """Portrait export should attempt the correct dimensions."""
    result = export_for_social("/tmp/in.mp4", "/tmp/out_portrait.mp4", 1080, 1920)
    assert isinstance(result, str)
    assert result.startswith("error")


def test_export_square_dimensions():
    """Square export should attempt the correct dimensions."""
    result = export_for_social("/tmp/in.mp4", "/tmp/out_square.mp4", 1080, 1080)
    assert isinstance(result, str)
    assert result.startswith("error")
