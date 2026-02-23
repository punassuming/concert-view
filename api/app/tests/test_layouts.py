import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.layouts import _layouts


@pytest.fixture(autouse=True)
def clear_layouts():
    _layouts.clear()
    yield
    _layouts.clear()


@pytest.mark.asyncio
async def test_create_layout():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/layouts/",
            json={
                "name": "2x2 Grid",
                "slots": [
                    {"feed_id": "f1", "x": 0.0, "y": 0.0, "width": 0.5, "height": 0.5},
                    {"feed_id": "f2", "x": 0.5, "y": 0.0, "width": 0.5, "height": 0.5},
                    {"feed_id": "f3", "x": 0.0, "y": 0.5, "width": 0.5, "height": 0.5},
                    {"feed_id": "f4", "x": 0.5, "y": 0.5, "width": 0.5, "height": 0.5},
                ],
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "2x2 Grid"
    assert len(data["slots"]) == 4


@pytest.mark.asyncio
async def test_list_layouts():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post(
            "/api/layouts/",
            json={
                "name": "L1",
                "slots": [
                    {"feed_id": "f1", "x": 0, "y": 0, "width": 1, "height": 1}
                ],
            },
        )
        resp = await client.get("/api/layouts/")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


@pytest.mark.asyncio
async def test_suggest_layout_fallback():
    """Without AI keys, the suggest endpoint should return a fallback layout."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/layouts/suggest",
            json={"feed_count": 4, "style": "grid"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "layout" in data
    assert "description" in data
    assert len(data["layout"]["slots"]) == 4
