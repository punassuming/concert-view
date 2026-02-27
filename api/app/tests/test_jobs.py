from unittest.mock import MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_get_job_status_pending():
    """A job_id that has no result yet should return PENDING state."""
    with patch("app.routers.jobs.AsyncResult") as mock_result_cls:
        mock_result = MagicMock()
        mock_result.state = "PENDING"
        mock_result.ready.return_value = False
        mock_result_cls.return_value = mock_result

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.get("/api/jobs/some-job-id")

    assert resp.status_code == 200
    data = resp.json()
    assert data["job_id"] == "some-job-id"
    assert data["state"] == "PENDING"
    assert "result" not in data
    assert "error" not in data


@pytest.mark.asyncio
async def test_get_job_status_success():
    """A completed successful job should include the result."""
    with patch("app.routers.jobs.AsyncResult") as mock_result_cls:
        mock_result = MagicMock()
        mock_result.state = "SUCCESS"
        mock_result.ready.return_value = True
        mock_result.successful.return_value = True
        mock_result.result = {"offset_seconds": 1.5, "confidence": 0.9}
        mock_result_cls.return_value = mock_result

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.get("/api/jobs/some-job-id")

    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "SUCCESS"
    assert data["result"]["offset_seconds"] == 1.5


@pytest.mark.asyncio
async def test_get_job_status_failure():
    """A failed job should include the error message."""
    with patch("app.routers.jobs.AsyncResult") as mock_result_cls:
        mock_result = MagicMock()
        mock_result.state = "FAILURE"
        mock_result.ready.return_value = True
        mock_result.successful.return_value = False
        mock_result.result = RuntimeError("ffmpeg not available")
        mock_result_cls.return_value = mock_result

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.get("/api/jobs/bad-job-id")

    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "FAILURE"
    assert "ffmpeg" in data["error"]


@pytest.mark.asyncio
async def test_dispatch_compose():
    """POST /api/jobs/compose should return 202 with a job_id."""
    with patch("app.routers.jobs.celery_app") as mock_celery:
        mock_task = MagicMock()
        mock_task.id = "task-compose-1"
        mock_celery.send_task.return_value = mock_task

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/jobs/compose",
                json={
                    "layout": {"output_width": 1920, "output_height": 1080, "slots": []},
                    "feed_paths": {"feed-1": "/data/uploads/a.mp4"},
                    "output_filename": "out.mp4",
                },
            )

    assert resp.status_code == 202
    data = resp.json()
    assert data["job_id"] == "task-compose-1"
    assert data["state"] == "PENDING"


@pytest.mark.asyncio
async def test_dispatch_sync():
    """POST /api/jobs/sync should return 202 with a job_id."""
    with patch("app.routers.jobs.celery_app") as mock_celery:
        mock_task = MagicMock()
        mock_task.id = "task-sync-1"
        mock_celery.send_task.return_value = mock_task

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/jobs/sync",
                json={
                    "reference_path": "/data/uploads/ref.mp4",
                    "target_path": "/data/uploads/tgt.mp4",
                },
            )

    assert resp.status_code == 202
    data = resp.json()
    assert data["job_id"] == "task-sync-1"


@pytest.mark.asyncio
async def test_dispatch_optimize():
    """POST /api/jobs/optimize should return 202 with a job_id."""
    with patch("app.routers.jobs.celery_app") as mock_celery:
        mock_task = MagicMock()
        mock_task.id = "task-opt-1"
        mock_celery.send_task.return_value = mock_task

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            resp = await client.post(
                "/api/jobs/optimize",
                json={
                    "input_path": "/data/uploads/in.mp4",
                    "output_filename": "out_norm.mp4",
                    "normalize": True,
                    "noise_reduce": False,
                },
            )

    assert resp.status_code == 202
    data = resp.json()
    assert data["job_id"] == "task-opt-1"
