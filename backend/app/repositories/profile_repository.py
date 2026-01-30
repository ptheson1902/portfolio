"""Profile repository for database access."""
from typing import Dict, Any, Optional
from datetime import date
from sqlalchemy.orm import Session

from ..models.db_models import Profile, RoleEmphasis
from ..models.schemas import Language, Role
from .base import BaseRepository


def calculate_age(birth_date_str: str) -> int:
    """Calculate age from date of birth string (YYYY-MM-DD)."""
    if not birth_date_str:
        return 0
    try:
        birth_date = date.fromisoformat(birth_date_str)
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    except ValueError:
        return 0


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

        # Calculate age from date of birth
        age = calculate_age(profile.date_of_birth) if profile.date_of_birth else 0

        # Extract language-specific address
        address = ""
        if profile.address:
            address = profile.address.get(lang.value, profile.address.get("ja", ""))

        # Extract language-specific work_experience
        work_experience = ""
        if profile.work_experience:
            if isinstance(profile.work_experience, dict):
                work_experience = profile.work_experience.get(lang.value, profile.work_experience.get("ja", ""))
            else:
                work_experience = profile.work_experience

        # Extract language-specific japan_residence
        japan_residence = ""
        if profile.japan_residence:
            if isinstance(profile.japan_residence, dict):
                japan_residence = profile.japan_residence.get(lang.value, profile.japan_residence.get("ja", ""))
            else:
                japan_residence = profile.japan_residence

        return {
            "name": profile.name,
            "name_kana": profile.name_kana,
            "name_vi": profile.name_vi,
            "gender": profile.gender,
            "date_of_birth": profile.date_of_birth,
            "age": age,
            "school": profile.school,
            "graduation_year": profile.graduation_year,
            "field": profile.field,
            "work_experience": work_experience,
            "japan_residence": japan_residence,
            "japanese_level": profile.japanese_level,
            "email": profile.email,
            "phone": profile.phone,
            "address": address,
            "social_links": profile.social_links,
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

    def update_address(self, lang: Language, content: str) -> Optional[Profile]:
        """Update address for a specific language."""
        profile = self.get_profile()
        if profile:
            if not profile.address:
                profile.address = {}
            address = dict(profile.address)
            address[lang.value] = content
            profile.address = address
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
