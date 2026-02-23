import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.feeds import _feeds
from app.models.feed import Feed


@pytest.fixture(autouse=True)
def setup_feeds():
    _feeds.clear()
    f1 = Feed(name="Cam1", source_url="http://a", id="feed-1")
    f2 = Feed(name="Cam2", source_url="http://b", id="feed-2")
    _feeds["feed-1"] = f1
    _feeds["feed-2"] = f2
    yield
    _feeds.clear()


@pytest.mark.asyncio
async def test_audio_sync():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/audio/sync",
            json={"feed_ids": ["feed-1", "feed-2"]},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert data[0]["feed_id"] == "feed-1"
    assert "detected_offset_seconds" in data[0]
    assert "confidence" in data[0]


@pytest.mark.asyncio
async def test_audio_optimize():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/audio/optimize",
            json={
                "feed_ids": ["feed-1", "feed-2"],
                "master_feed_id": "feed-1",
                "normalize": True,
                "noise_reduce": False,
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "output_path" in data
    assert data["settings_applied"]["normalize"] is True
