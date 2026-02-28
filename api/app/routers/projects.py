import os

from fastapi import APIRouter, HTTPException, Query

from app.celery_app import celery_app
from app.config import settings
from app.models.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])

_projects: dict[str, Project] = {}


@router.get("/")
async def list_projects() -> list[Project]:
    return list(_projects.values())


@router.post("/", status_code=201)
async def create_project(body: ProjectCreate) -> Project:
    project = Project(
        name=body.name,
        clips=body.clips,
        output_width=body.output_width or 1920,
        output_height=body.output_height or 1080,
    )
    _projects[project.id] = project
    return project


@router.get("/{project_id}")
async def get_project(project_id: str) -> Project:
    project = _projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}")
async def update_project(project_id: str, body: ProjectUpdate) -> Project:
    project = _projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = body.model_dump(exclude_unset=True)
    updated = project.model_copy(update=update_data)
    _projects[project_id] = updated
    return updated


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str):
    if project_id not in _projects:
        raise HTTPException(status_code=404, detail="Project not found")
    del _projects[project_id]
    return None


@router.post("/{project_id}/render", status_code=202)
async def render_project(
    project_id: str,
    feed_paths: dict[str, str],
    output_filename: str = Query(..., description="Filename for the rendered output video"),
) -> dict:
    """Dispatch a render job for the project timeline."""
    project = _projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    output_path = os.path.join(settings.OUTPUT_DIR, output_filename)
    task = celery_app.send_task(
        "processor.celery_app.render_timeline_task",
        args=[project.model_dump(), feed_paths, output_path],
    )
    return {"job_id": task.id, "state": "PENDING"}
