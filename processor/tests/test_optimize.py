from processor.optimize import normalize_audio, optimize_audio


def test_normalize_handles_missing_ffmpeg():
    """normalize_audio should return an error string when ffmpeg is missing."""
    result = normalize_audio("/nonexistent/in.wav", "/tmp/out.wav")
    assert isinstance(result, str)
    assert result.startswith("error")


def test_optimize_returns_settings():
    """optimize_audio should always return the settings that were requested."""
    result = optimize_audio("/nonexistent/in.wav", "/tmp/out.wav", normalize=True, noise_reduce=False)
    assert isinstance(result, dict)
    assert result["normalize"] is True
    assert result["noise_reduce"] is False
    assert "result" in result
