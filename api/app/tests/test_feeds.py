import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.feeds import _feeds


@pytest.fixture(autouse=True)
def clear_feeds():
    _feeds.clear()
    yield
    _feeds.clear()


@pytest.mark.asyncio
async def test_create_feed():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/feeds/",
            json={"name": "Main Stage", "source_url": "rtmp://example.com/live"},
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Main Stage"
    assert data["source_url"] == "rtmp://example.com/live"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_feeds():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/feeds/", json={"name": "Cam1", "source_url": "http://a"}
        )
        await client.post(
            "/api/feeds/", json={"name": "Cam2", "source_url": "http://b"}
        )
        resp = await client.get("/api/feeds/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_feed():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post(
            "/api/feeds/", json={"name": "Cam1", "source_url": "http://a"}
        )
        feed_id = create_resp.json()["id"]
        resp = await client.get(f"/api/feeds/{feed_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == feed_id


@pytest.mark.asyncio
async def test_update_feed():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post(
            "/api/feeds/", json={"name": "Cam1", "source_url": "http://a"}
        )
        feed_id = create_resp.json()["id"]
        resp = await client.patch(
            f"/api/feeds/{feed_id}",
            json={"name": "Updated Cam", "volume": 0.8},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated Cam"
    assert data["volume"] == 0.8


@pytest.mark.asyncio
async def test_delete_feed():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post(
            "/api/feeds/", json={"name": "Cam1", "source_url": "http://a"}
        )
        feed_id = create_resp.json()["id"]
        resp = await client.delete(f"/api/feeds/{feed_id}")
        assert resp.status_code == 204
        get_resp = await client.get(f"/api/feeds/{feed_id}")
    assert get_resp.status_code == 404
