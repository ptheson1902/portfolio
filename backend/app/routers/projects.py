"""Projects router with CRUD operations."""
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any, Dict

from ..database.connection import get_db
from ..models.schemas import (
    Role, Language, ProjectsResponse, ProjectCreate, ProjectUpdate,
    ProjectBrief, MessageResponse
)
from ..services.project_service import ProjectService
from ..middleware.auth_middleware import require_owner

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=ProjectsResponse)
async def get_projects(
    lang: Language = Query(Language.JA, description="Language for response"),
    role: Role = Query(Role.FULLSTACK, description="Target role perspective"),
    db: Session = Depends(get_db)
):
    """
    Get all projects sorted by role relevance.
    Public endpoint - no authentication required.
    """
    service = ProjectService(db)
    return service.get_projects(lang, role)


@router.get("/all")
async def get_all_projects_raw(
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
) -> List[Dict[str, Any]]:
    """
    Get all projects with raw data for admin editing.
    Protected endpoint - requires OWNER role.
    """
    service = ProjectService(db)
    return service.get_all_projects_raw()


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get a single project by ID with all fields.
    Public endpoint - no authentication required.
    """
    service = ProjectService(db)
    project = service.get_project_for_edit(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectBrief)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Create a new project.
    Protected endpoint - requires OWNER role.
    """
    service = ProjectService(db)
    try:
        project = service.create_project({
            "name": project_data.name.model_dump(),
            "description": project_data.description.model_dump(),
            "highlights": project_data.highlights.model_dump(),
            "role": project_data.role,
            "team_size": project_data.team_size,
            "technologies": project_data.technologies,
            "environment": project_data.environment,
            "phases": project_data.phases,
            "start_date": project_data.start_date,
            "duration": project_data.duration,
            "end_date": project_data.end_date,
            "relevance_leader": project_data.relevance_leader,
            "relevance_brse": project_data.relevance_brse,
            "relevance_fullstack": project_data.relevance_fullstack
        })
        return ProjectBrief(
            id=project["id"],
            name=project_data.name,
            role=project_data.role
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{project_id}", response_model=MessageResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Update an existing project.
    Protected endpoint - requires OWNER role.
    """
    service = ProjectService(db)

    # Build update dict from non-None values
    update_dict = {}
    if project_data.name is not None:
        update_dict["name"] = project_data.name.model_dump()
    if project_data.description is not None:
        update_dict["description"] = project_data.description.model_dump()
    if project_data.highlights is not None:
        update_dict["highlights"] = project_data.highlights.model_dump()
    if project_data.role is not None:
        update_dict["role"] = project_data.role
    if project_data.team_size is not None:
        update_dict["team_size"] = project_data.team_size
    if project_data.technologies is not None:
        update_dict["technologies"] = project_data.technologies
    if project_data.environment is not None:
        update_dict["environment"] = project_data.environment
    if project_data.phases is not None:
        update_dict["phases"] = project_data.phases
    if project_data.start_date is not None:
        update_dict["start_date"] = project_data.start_date
    if project_data.duration is not None:
        update_dict["duration"] = project_data.duration
    if project_data.end_date is not None:
        update_dict["end_date"] = project_data.end_date
    if project_data.relevance_leader is not None:
        update_dict["relevance_leader"] = project_data.relevance_leader
    if project_data.relevance_brse is not None:
        update_dict["relevance_brse"] = project_data.relevance_brse
    if project_data.relevance_fullstack is not None:
        update_dict["relevance_fullstack"] = project_data.relevance_fullstack

    project = service.update_project(project_id, update_dict)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return MessageResponse(success=True, message="Project updated successfully")


@router.delete("/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Delete a project.
    Protected endpoint - requires OWNER role.
    """
    service = ProjectService(db)
    deleted = service.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return MessageResponse(success=True, message="Project deleted successfully")
