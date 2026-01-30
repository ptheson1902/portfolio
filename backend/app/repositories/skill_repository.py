"""Skill repository for database access."""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from ..models.db_models import Skill, SkillCategory
from ..models.schemas import Language, Role
from .base import BaseRepository


class SkillRepository(BaseRepository[Skill]):
    """Repository for Skill operations."""

    def __init__(self, db: Session):
        super().__init__(Skill, db)

    def get_skills_by_category(self, category_key: str) -> List[Skill]:
        """Get all skills in a specific category."""
        return self.db.query(Skill).filter(
            Skill.category_key == category_key
        ).order_by(Skill.display_order).all()

    def get_skills_grouped_by_category(self, lang: Language, role: Role) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get skills grouped by category.
        For LEADER role, skills are sorted by level (descending).
        """
        categories = self.db.query(SkillCategory).order_by(
            SkillCategory.display_order
        ).all()

        result = {}
        for cat in categories:
            skills = self.db.query(Skill).filter(
                Skill.category_id == cat.id
            ).order_by(Skill.display_order).all()

            skill_list = [
                {
                    "id": s.id,
                    "name": s.name,
                    "level": s.level,
                    "experience": s.experience,
                    "category": s.category_key
                }
                for s in skills
            ]

            # Sort by level for LEADER role
            if role == Role.LEADER:
                skill_list = sorted(skill_list, key=lambda x: (-x["level"], x["name"]))

            result[cat.key] = skill_list

        return result

    def get_all_skills_flat(self) -> List[Dict[str, Any]]:
        """Get all skills as a flat list."""
        skills = self.db.query(Skill).order_by(
            Skill.category_key, Skill.display_order
        ).all()

        return [
            {
                "id": s.id,
                "name": s.name,
                "level": s.level,
                "experience": s.experience,
                "category": s.category_key
            }
            for s in skills
        ]

    def create_skill(self, name: str, level: int, experience: str, category_key: str) -> Skill:
        """Create a new skill."""
        # Get category
        category = self.db.query(SkillCategory).filter(
            SkillCategory.key == category_key
        ).first()

        if not category:
            raise ValueError(f"Category '{category_key}' not found")

        # Get next display order
        max_order = self.db.query(Skill).filter(
            Skill.category_id == category.id
        ).count()

        skill = Skill(
            name=name,
            level=level,
            experience=experience,
            category_id=category.id,
            category_key=category_key,
            display_order=max_order
        )
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def update_skill(self, id: int, **kwargs) -> Optional[Skill]:
        """Update a skill."""
        skill = self.get(id)
        if skill:
            # Handle category change
            if "category_key" in kwargs and kwargs["category_key"] != skill.category_key:
                category = self.db.query(SkillCategory).filter(
                    SkillCategory.key == kwargs["category_key"]
                ).first()
                if category:
                    skill.category_id = category.id
                    skill.category_key = kwargs["category_key"]
                del kwargs["category_key"]

            for key, value in kwargs.items():
                if hasattr(skill, key) and value is not None:
                    setattr(skill, key, value)

            self.db.commit()
            self.db.refresh(skill)
        return skill


class SkillCategoryRepository(BaseRepository[SkillCategory]):
    """Repository for SkillCategory operations."""

    def __init__(self, db: Session):
        super().__init__(SkillCategory, db)

    def get_by_key(self, key: str) -> Optional[SkillCategory]:
        """Get category by key."""
        return self.db.query(SkillCategory).filter(
            SkillCategory.key == key
        ).first()

    def get_all_ordered(self) -> List[SkillCategory]:
        """Get all categories ordered by display_order."""
        return self.db.query(SkillCategory).order_by(
            SkillCategory.display_order
        ).all()
