"""Skills router with CRUD operations."""
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database.connection import get_db
from ..models.schemas import (
    Role, Language, SkillsResponse, SkillCreate, SkillUpdate,
    SkillResponse, MessageResponse
)
from ..services.skill_service import SkillService
from ..middleware.auth_middleware import require_owner

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("", response_model=SkillsResponse)
async def get_skills(
    lang: Language = Query(Language.JA, description="Language for response"),
    role: Role = Query(Role.FULLSTACK, description="Target role perspective"),
    db: Session = Depends(get_db)
):
    """
    Get all skills grouped by category.
    Public endpoint - no authentication required.
    """
    service = SkillService(db)
    return service.get_skills(lang, role)


@router.get("/all", response_model=List[SkillResponse])
async def get_all_skills(
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Get all skills as flat list for admin.
    Protected endpoint - requires OWNER role.
    """
    service = SkillService(db)
    skills = service.get_all_skills()
    return [SkillResponse(**s) for s in skills]


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single skill by ID.
    Public endpoint - no authentication required.
    """
    service = SkillService(db)
    skill = service.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return SkillResponse(**skill)


@router.post("", response_model=SkillResponse)
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Create a new skill.
    Protected endpoint - requires OWNER role.
    """
    service = SkillService(db)
    try:
        skill = service.create_skill(
            name=skill_data.name,
            level=skill_data.level,
            experience=skill_data.experience,
            category=skill_data.category
        )
        return SkillResponse(**skill)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: int,
    skill_data: SkillUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Update an existing skill.
    Protected endpoint - requires OWNER role.
    """
    service = SkillService(db)
    skill = service.update_skill(
        skill_id=skill_id,
        name=skill_data.name,
        level=skill_data.level,
        experience=skill_data.experience,
        category=skill_data.category
    )
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return SkillResponse(**skill)


@router.delete("/{skill_id}", response_model=MessageResponse)
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Delete a skill.
    Protected endpoint - requires OWNER role.
    """
    service = SkillService(db)
    deleted = service.delete_skill(skill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Skill not found")
    return MessageResponse(success=True, message="Skill deleted successfully")
