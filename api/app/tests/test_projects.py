import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routers.projects import _projects


@pytest.fixture(autouse=True)
def clear_projects():
    _projects.clear()
    yield
    _projects.clear()


@pytest.mark.asyncio
async def test_create_project():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/projects/",
            json={"name": "Concert Edit", "clips": []},
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Concert Edit"
    assert data["clips"] == []
    assert "id" in data


@pytest.mark.asyncio
async def test_create_project_with_clips():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.post(
            "/api/projects/",
            json={
                "name": "My Concert",
                "clips": [
                    {"feed_id": "feed-1", "timeline_start": 0.0, "trim_start": 10.0, "trim_end": 60.0},
                    {"feed_id": "feed-2", "timeline_start": 50.0},
                ],
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["clips"]) == 2
    assert data["clips"][0]["trim_start"] == 10.0
    assert data["clips"][0]["trim_end"] == 60.0
    assert data["clips"][1]["trim_start"] is None


@pytest.mark.asyncio
async def test_list_projects():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        await client.post("/api/projects/", json={"name": "P1"})
        await client.post("/api/projects/", json={"name": "P2"})
        resp = await client.get("/api/projects/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_get_project():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post("/api/projects/", json={"name": "P1"})
        project_id = create_resp.json()["id"]
        resp = await client.get(f"/api/projects/{project_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == project_id


@pytest.mark.asyncio
async def test_get_project_not_found():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/projects/nonexistent")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_project():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post("/api/projects/", json={"name": "Original"})
        project_id = create_resp.json()["id"]
        resp = await client.patch(
            f"/api/projects/{project_id}",
            json={"name": "Updated", "clips": [{"feed_id": "f1", "timeline_start": 0.0}]},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Updated"
    assert len(data["clips"]) == 1


@pytest.mark.asyncio
async def test_delete_project():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        create_resp = await client.post("/api/projects/", json={"name": "ToDelete"})
        project_id = create_resp.json()["id"]
        resp = await client.delete(f"/api/projects/{project_id}")
        assert resp.status_code == 204
        get_resp = await client.get(f"/api/projects/{project_id}")
    assert get_resp.status_code == 404
