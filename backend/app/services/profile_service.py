"""Profile service for business logic."""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..models.schemas import Language, Role, ProfileResponse, Profile as ProfileSchema
from ..repositories.profile_repository import ProfileRepository


class ProfileService:
    """Service for profile business logic."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ProfileRepository(db)

    def get_profile(self, lang: Language, role: Role) -> ProfileResponse:
        """Get profile formatted for API response."""
        profile_data = self.repo.get_profile_for_display(lang, role)

        if not profile_data:
            raise ValueError("Profile not found")

        profile = ProfileSchema(
            name=profile_data["name"],
            name_kana=profile_data["name_kana"],
            gender=profile_data["gender"],
            age=profile_data["age"],
            school=f"{profile_data['school']} ({profile_data['graduation_year']})",
            field=profile_data["field"],
            work_experience=profile_data["work_experience"],
            japan_residence=profile_data["japan_residence"],
            japanese_level=profile_data["japanese_level"],
            self_pr=profile_data["self_pr"]
        )

        return ProfileResponse(
            profile=profile,
            role_emphasis=profile_data["role_emphasis"]
        )

    def get_profile_raw(self) -> Optional[Dict[str, Any]]:
        """Get raw profile data for admin editing."""
        profile = self.repo.get_profile()
        if not profile:
            return None

        return {
            "id": profile.id,
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
            "self_pr": profile.self_pr
        }

    def update_profile(self, update_data: Dict[str, Any], lang: Language, role: Role) -> ProfileResponse:
        """Update profile and return updated data."""
        # Filter out None values
        update_dict = {k: v for k, v in update_data.items() if v is not None}

        self.repo.update_profile(**update_dict)
        return self.get_profile(lang, role)

    def update_self_pr(self, lang: Language, content: str, role: Role) -> ProfileResponse:
        """Update self_pr for a specific language."""
        self.repo.update_self_pr(lang, content)
        return self.get_profile(lang, role)
