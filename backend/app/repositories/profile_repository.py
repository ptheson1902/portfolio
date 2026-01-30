"""Profile repository for database access."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models.db_models import Profile, RoleEmphasis
from ..models.schemas import Language, Role
from .base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    """Repository for Profile operations."""

    def __init__(self, db: Session):
        super().__init__(Profile, db)

    def get_profile(self) -> Optional[Profile]:
        """Get the profile (single profile system)."""
        return self.db.query(Profile).first()

    def get_profile_for_display(self, lang: Language, role: Role) -> Optional[Dict[str, Any]]:
        """
        Get profile with language-specific fields extracted.
        Returns a dictionary ready for API response.
        """
        profile = self.get_profile()
        if not profile:
            return None

        # Extract language-specific self_pr
        self_pr = ""
        if profile.self_pr:
            self_pr = profile.self_pr.get(lang.value, profile.self_pr.get("ja", ""))

        # Get role emphasis keywords
        role_emphasis = self.db.query(RoleEmphasis).filter(
            RoleEmphasis.role == role.value
        ).first()

        emphasis_keywords = []
        if role_emphasis and role_emphasis.keywords:
            emphasis_keywords = role_emphasis.keywords.get(lang.value, [])

        return {
            "name": profile.name,
            "name_kana": profile.name_kana,
            "name_vi": profile.name_vi,
            "gender": profile.gender,
            "age": profile.age,
            "school": profile.school,
            "graduation_year": profile.graduation_year,
            "field": profile.field,
            "work_experience": profile.work_experience,
            "japan_residence": profile.japan_residence,
            "japanese_level": profile.japanese_level,
            "self_pr": self_pr,
            "role_emphasis": emphasis_keywords
        }

    def update_profile(self, **kwargs) -> Optional[Profile]:
        """Update the profile."""
        profile = self.get_profile()
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key) and value is not None:
                    setattr(profile, key, value)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_self_pr(self, lang: Language, content: str) -> Optional[Profile]:
        """Update self_pr for a specific language."""
        profile = self.get_profile()
        if profile:
            if not profile.self_pr:
                profile.self_pr = {}
            self_pr = dict(profile.self_pr)
            self_pr[lang.value] = content
            profile.self_pr = self_pr
            self.db.commit()
            self.db.refresh(profile)
        return profile
