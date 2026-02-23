from processor.sync import detect_offset, extract_audio_pcm


def test_detect_offset_mock():
    """When ffmpeg is not available or files don't exist, return mock data."""
    result = detect_offset("/nonexistent/ref.mp4", "/nonexistent/tgt.mp4")
    assert "offset_seconds" in result
    assert "confidence" in result
    assert result["confidence"] == 0.0


def test_extract_audio_handles_missing_file():
    """Gracefully return an empty array for a missing file."""
    samples = extract_audio_pcm("/nonexistent/video.mp4")
    assert samples.size == 0
