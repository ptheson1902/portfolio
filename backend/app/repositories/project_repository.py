"""Project repository for database access."""
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.db_models import Project
from ..models.schemas import Language, Role
from .base import BaseRepository


def calculate_duration(start_date: str, end_date: Optional[str], lang: Language) -> str:
    """
    Calculate duration from start_date and end_date.
    Returns multilingual duration string based on lang.
    Format: YYYY-MM for both dates.
    """
    if not start_date:
        return ""

    try:
        start = datetime.strptime(start_date, "%Y-%m")
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m")
        else:
            end = datetime.now()

        # Calculate months difference (inclusive of both start and end month)
        months = (end.year - start.year) * 12 + (end.month - start.month) + 1
        if months < 1:
            months = 1

        years = months // 12
        remaining_months = months % 12

        # Format based on language
        if lang == Language.JA:
            if years > 0 and remaining_months > 0:
                return f"{years}年{remaining_months}ヶ月"
            elif years > 0:
                return f"{years}年"
            else:
                return f"{remaining_months}ヶ月"
        elif lang == Language.VI:
            if years > 0 and remaining_months > 0:
                return f"{years} năm {remaining_months} tháng"
            elif years > 0:
                return f"{years} năm"
            else:
                return f"{remaining_months} tháng"
        else:  # EN
            if years > 0 and remaining_months > 0:
                return f"{years}y {remaining_months}m"
            elif years > 0:
                return f"{years}y"
            else:
                return f"{remaining_months}m"
    except ValueError:
        return ""


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project operations."""

    def __init__(self, db: Session):
        super().__init__(Project, db)

    def _extract_multilingual(self, value: Any, lang: Language, default: Any = "") -> Any:
        """Extract language-specific value from multilingual field."""
        if isinstance(value, dict):
            return value.get(lang.value, value.get("ja", default))
        return value or default

    def _get_duration(self, start_date: str, end_date: Optional[str], lang: Language) -> str:
        """Calculate duration from dates."""
        return calculate_duration(start_date, end_date, lang)

    def get_projects_for_display(self, lang: Language, role: Role) -> Dict[str, Any]:
        """
        Get projects with language-specific fields extracted.
        Projects are sorted by role relevance.
        Duration is auto-calculated from start_date and end_date.
        """
        projects = self.db.query(Project).all()

        project_list = []
        for p in projects:
            # Extract language-specific fields
            name = self._extract_multilingual(p.name, lang)
            description = self._extract_multilingual(p.description, lang)
            highlights = self._extract_multilingual(p.highlights, lang, [])
            # Auto-calculate duration from dates
            duration = self._get_duration(p.start_date, p.end_date, lang)

            project_list.append({
                "id": p.id,
                "name": name,
                "role": p.role,
                "team_size": p.team_size,
                "technologies": p.technologies or [],
                "environment": p.environment,
                "phases": p.phases or [],
                "start_date": p.start_date,
                "end_date": p.end_date,
                "duration": duration,
                "description": description,
                "highlights": highlights,
                "relevance": p.get_relevance(role.value)
            })

        # Sort by relevance (descending) then by ID (descending)
        project_list = sorted(
            project_list,
            key=lambda x: (-x["relevance"], -x["id"])
        )

        # Get top 3 highlighted project IDs
        highlighted = [p["id"] for p in project_list[:3]]

        return {
            "projects": project_list,
            "highlighted": highlighted
        }

    def get_all_projects_raw(self) -> List[Project]:
        """Get all projects with raw data (for admin/export)."""
        return self.db.query(Project).order_by(Project.id).all()

    def get_project_for_edit(self, id: int) -> Optional[Dict[str, Any]]:
        """Get a project with all fields for editing."""
        project = self.get(id)
        if not project:
            return None

        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "highlights": project.highlights,
            "role": project.role,
            "team_size": project.team_size,
            "technologies": project.technologies,
            "environment": project.environment,
            "phases": project.phases,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "duration": project.duration,
            "relevance_leader": project.relevance_leader,
            "relevance_brse": project.relevance_brse,
            "relevance_fullstack": project.relevance_fullstack
        }

    def create_project(
        self,
        name: Dict[str, str],
        description: Dict[str, str],
        highlights: Dict[str, List[str]],
        role: str,
        team_size: str,
        technologies: List[str],
        environment: str,
        phases: List[str],
        start_date: str,
        end_date: Optional[str] = None,
        relevance_leader: int = 1,
        relevance_brse: int = 1,
        relevance_fullstack: int = 1
    ) -> Project:
        """Create a new project. Duration is auto-calculated from dates."""
        # Get next ID
        max_id = self.db.query(Project).count() + 1

        project = Project(
            id=max_id,
            name=name,
            description=description,
            highlights=highlights,
            role=role,
            team_size=team_size,
            technologies=technologies,
            environment=environment,
            phases=phases,
            start_date=start_date,
            end_date=end_date,
            relevance_leader=relevance_leader,
            relevance_brse=relevance_brse,
            relevance_fullstack=relevance_fullstack,
            display_order=max_id
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update_project(self, id: int, **kwargs) -> Optional[Project]:
        """Update a project."""
        project = self.get(id)
        if project:
            for key, value in kwargs.items():
                if hasattr(project, key) and value is not None:
                    setattr(project, key, value)
            self.db.commit()
            self.db.refresh(project)
        return project

    def get_projects_for_resume(self, lang: Language) -> List[Dict[str, Any]]:
        """Get projects formatted for resume export."""
        projects = self.db.query(Project).order_by(Project.start_date.desc()).all()

        return [
            {
                "name": self._extract_multilingual(p.name, lang),
                "role": p.role,
                "team_size": p.team_size,
                "technologies": p.technologies or [],
                "phases": p.phases or [],
                "start_date": p.start_date,
                "end_date": p.end_date,
                "duration": self._get_duration(p.start_date, p.end_date, lang),
                "description": self._extract_multilingual(p.description, lang),
                "highlights": self._extract_multilingual(p.highlights, lang, [])
            }
            for p in projects
        ]
