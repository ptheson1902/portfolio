"""Profile router with CRUD operations."""
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.schemas import (
    Role, Language, ProfileResponse, ProfileUpdate,
    SelfPrUpdate, MessageResponse
)
from ..services.profile_service import ProfileService
from ..middleware.auth_middleware import require_owner

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
async def get_profile(
    lang: Language = Query(Language.JA, description="Language for response"),
    role: Role = Query(Role.FULLSTACK, description="Target role perspective"),
    db: Session = Depends(get_db)
):
    """
    Get profile information.
    Public endpoint - no authentication required.
    """
    service = ProfileService(db)
    try:
        return service.get_profile(lang, role)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("", response_model=ProfileResponse)
async def update_profile(
    update_data: ProfileUpdate,
    lang: Language = Query(Language.JA, description="Language for response"),
    role: Role = Query(Role.FULLSTACK, description="Target role perspective"),
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Update profile information.
    Protected endpoint - requires OWNER role.
    """
    service = ProfileService(db)
    try:
        return service.update_profile(update_data.model_dump(exclude_none=True), lang, role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/self-pr", response_model=ProfileResponse)
async def update_self_pr(
    update_data: SelfPrUpdate,
    lang: Language = Query(Language.JA, description="Language to update"),
    role: Role = Query(Role.FULLSTACK, description="Target role perspective"),
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Update self PR for a specific language.
    Protected endpoint - requires OWNER role.
    """
    service = ProfileService(db)
    try:
        return service.update_self_pr(lang, update_data.content, role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/raw")
async def get_profile_raw(
    db: Session = Depends(get_db),
    _: None = Depends(require_owner)
):
    """
    Get raw profile data for admin editing.
    Protected endpoint - requires OWNER role.
    """
    service = ProfileService(db)
    data = service.get_profile_raw()
    if not data:
        raise HTTPException(status_code=404, detail="Profile not found")
    return data
