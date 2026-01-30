"""Project service for business logic."""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from ..models.schemas import Language, Role, ProjectsResponse, Project as ProjectSchema
from ..repositories.project_repository import ProjectRepository


class ProjectService:
    """Service for project business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ProjectRepository(db)

    def get_projects(self, lang: Language, role: Role) -> ProjectsResponse:
        """Get projects formatted for API response."""
        projects_data = self.repo.get_projects_for_display(lang, role)

        projects = [
            ProjectSchema(
                id=p["id"],
                name=p["name"],
                role=p["role"],
                team_size=p["team_size"],
                technologies=p["technologies"],
                environment=p["environment"],
                phases=p["phases"],
                start_date=p["start_date"],
                end_date=p["end_date"],
                duration=p["duration"],
                description=p["description"],
                highlights=p["highlights"]
            )
            for p in projects_data["projects"]
        ]

        return ProjectsResponse(
            projects=projects,
            highlighted=projects_data["highlighted"]
        )

    def get_project_for_edit(self, project_id: int) -> Optional[Dict[str, Any]]:
        """Get a project with all fields for editing."""
        return self.repo.get_project_for_edit(project_id)

    def get_all_projects_raw(self) -> List[Dict[str, Any]]:
        """Get all projects with raw data for admin."""
        projects = self.repo.get_all_projects_raw()
        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "highlights": p.highlights,
                "role": p.role,
                "team_size": p.team_size,
                "technologies": p.technologies,
                "environment": p.environment,
                "phases": p.phases,
                "start_date": p.start_date,
                "end_date": p.end_date,
                "duration": p.duration,
                "relevance_leader": p.relevance_leader,
                "relevance_brse": p.relevance_brse,
                "relevance_fullstack": p.relevance_fullstack
            }
            for p in projects
        ]

    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project. Duration is auto-calculated from dates."""
        project = self.repo.create_project(
            name=project_data["name"],
            description=project_data["description"],
            highlights=project_data["highlights"],
            role=project_data["role"],
            team_size=project_data["team_size"],
            technologies=project_data["technologies"],
            environment=project_data["environment"],
            phases=project_data["phases"],
            start_date=project_data["start_date"],
            end_date=project_data.get("end_date"),
            relevance_leader=project_data.get("relevance_leader", 1),
            relevance_brse=project_data.get("relevance_brse", 1),
            relevance_fullstack=project_data.get("relevance_fullstack", 1)
        )

        return {
            "id": project.id,
            "name": project.name,
            "role": project.role
        }

    def update_project(self, project_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a project."""
        # Filter out None values
        filtered_data = {k: v for k, v in update_data.items() if v is not None}

        project = self.repo.update_project(project_id, **filtered_data)
        if not project:
            return None

        return {
            "id": project.id,
            "name": project.name,
            "role": project.role
        }

    def delete_project(self, project_id: int) -> bool:
        """Delete a project."""
        return self.repo.delete(project_id)

    def get_projects_for_resume(self, lang: Language) -> List[Dict[str, Any]]:
        """Get projects formatted for resume export."""
        return self.repo.get_projects_for_resume(lang)
