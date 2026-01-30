"""Skill service for business logic."""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from ..models.schemas import Language, Role, SkillsResponse, Skill as SkillSchema
from ..repositories.skill_repository import SkillRepository


class SkillService:
    """Service for skill business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = SkillRepository(db)

    def get_skills(self, lang: Language, role: Role) -> SkillsResponse:
        """Get skills formatted for API response."""
        skills_data = self.repo.get_skills_grouped_by_category(lang, role)

        def to_skill_schemas(skill_list: List[Dict]) -> List[SkillSchema]:
            return [
                SkillSchema(
                    id=s["id"],
                    name=s["name"],
                    level=s["level"],
                    experience=s["experience"],
                    category=s["category"]
                )
                for s in skill_list
            ]

        return SkillsResponse(
            programming_languages=to_skill_schemas(skills_data.get("programming_languages", [])),
            frameworks=to_skill_schemas(skills_data.get("frameworks", [])),
            databases=to_skill_schemas(skills_data.get("databases", [])),
            cloud=to_skill_schemas(skills_data.get("cloud", [])),
            other=to_skill_schemas(skills_data.get("ai_ml", []))
        )

    def get_all_skills(self) -> List[Dict[str, Any]]:
        """Get all skills as flat list for admin."""
        return self.repo.get_all_skills_flat()

    def get_skill(self, skill_id: int) -> Optional[Dict[str, Any]]:
        """Get a single skill by ID."""
        skill = self.repo.get(skill_id)
        if not skill:
            return None

        return {
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "experience": skill.experience,
            "category": skill.category_key
        }

    def create_skill(
        self,
        name: str,
        level: int,
        experience: str,
        category: str
    ) -> Dict[str, Any]:
        """Create a new skill."""
        skill = self.repo.create_skill(
            name=name,
            level=level,
            experience=experience,
            category_key=category
        )

        return {
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "experience": skill.experience,
            "category": skill.category_key
        }

    def update_skill(
        self,
        skill_id: int,
        name: Optional[str] = None,
        level: Optional[int] = None,
        experience: Optional[str] = None,
        category: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update an existing skill."""
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if level is not None:
            update_data["level"] = level
        if experience is not None:
            update_data["experience"] = experience
        if category is not None:
            update_data["category_key"] = category

        skill = self.repo.update_skill(skill_id, **update_data)
        if not skill:
            return None

        return {
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "experience": skill.experience,
            "category": skill.category_key
        }

    def delete_skill(self, skill_id: int) -> bool:
        """Delete a skill."""
        return self.repo.delete(skill_id)
