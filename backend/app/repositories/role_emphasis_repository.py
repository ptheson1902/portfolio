"""Role emphasis repository for database access."""
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models.db_models import RoleEmphasis
from ..models.schemas import Language, Role
from .base import BaseRepository


class RoleEmphasisRepository(BaseRepository[RoleEmphasis]):
    """Repository for RoleEmphasis operations."""

    def __init__(self, db: Session):
        super().__init__(RoleEmphasis, db)

    def get_by_role(self, role: Role) -> Optional[RoleEmphasis]:
        """Get role emphasis by role."""
        return self.db.query(RoleEmphasis).filter(
            RoleEmphasis.role == role.value
        ).first()

    def get_keywords(self, role: Role, lang: Language) -> List[str]:
        """Get emphasis keywords for a specific role and language."""
        emphasis = self.get_by_role(role)
        if emphasis and emphasis.keywords:
            return emphasis.keywords.get(lang.value, [])
        return []

    def update_keywords(self, role: Role, lang: Language, keywords: List[str]) -> Optional[RoleEmphasis]:
        """Update keywords for a specific role and language."""
        emphasis = self.get_by_role(role)
        if emphasis:
            if not emphasis.keywords:
                emphasis.keywords = {}
            keywords_dict = dict(emphasis.keywords)
            keywords_dict[lang.value] = keywords
            emphasis.keywords = keywords_dict
            self.db.commit()
            self.db.refresh(emphasis)
        return emphasis

    def get_all_role_emphasis(self) -> List[RoleEmphasis]:
        """Get all role emphasis records."""
        return self.db.query(RoleEmphasis).all()
