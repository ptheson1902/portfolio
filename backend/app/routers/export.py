"""Export router for resume generation."""
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from sqlalchemy.orm import Session
from io import BytesIO
from typing import Literal

from ..database.connection import get_db
from ..models.schemas import Language
from ..services.export_service import ExportService

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/resume")
async def export_resume(
    lang: Language = Query(Language.JA, description="Resume language (ja, vi, en)"),
    format: Literal["pdf", "docx", "html"] = Query("pdf", description="Output format"),
    db: Session = Depends(get_db)
):
    """
    Generate and download resume.

    - **lang**: Language for the resume (ja=Japanese, vi=Vietnamese, en=English)
    - **format**: Output format (pdf, docx, html)

    Returns the resume file as a download.
    """
    service = ExportService(db)

    try:
        content = service.generate_resume(lang, format)
    except ImportError as e:
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # Set filename and media type based on format
    filename = f"resume_{lang.value}.{format}"

    if format == "pdf":
        media_type = "application/pdf"
    elif format == "docx":
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:  # html
        # Return HTML directly for preview
        return HTMLResponse(content=content.decode("utf-8"))

    return StreamingResponse(
        BytesIO(content),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/resume/preview")
async def preview_resume(
    lang: Language = Query(Language.JA, description="Resume language (ja, vi, en)"),
    db: Session = Depends(get_db)
):
    """
    Preview resume as HTML.

    - **lang**: Language for the resume (ja=Japanese, vi=Vietnamese, en=English)

    Returns the resume as HTML for preview in browser.
    """
    service = ExportService(db)

    try:
        html_content = service.generate_html(lang)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return HTMLResponse(content=html_content)
