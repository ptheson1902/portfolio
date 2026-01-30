"""Export router for skill sheet generation."""
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from sqlalchemy.orm import Session
from io import BytesIO
from typing import Literal

from ..database.connection import get_db
from ..models.schemas import Language
from ..services.xlsx_export_service import XlsxExportService

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/resume")
async def export_resume(
    lang: Language = Query(Language.JA, description="Resume language (ja, vi, en)"),
    format: Literal["pdf", "html", "xlsx"] = Query("pdf", description="Output format"),
    db: Session = Depends(get_db)
):
    """
    Generate and download skill sheet (スキルシート).

    - **lang**: Language for the skill sheet (ja=Japanese, vi=Vietnamese, en=English)
    - **format**: Output format (pdf, html, xlsx)

    Returns the skill sheet file as a download or HTML preview.
    """
    service = XlsxExportService(db)

    try:
        if format == "xlsx":
            content = service.generate_xlsx(lang)
            filename = f"Skill_Sheet_{lang.value}.xlsx"
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format == "html":
            html_content = service.generate_html(lang)
            return HTMLResponse(content=html_content)
        else:  # pdf
            content = service.generate_pdf(lang)
            filename = f"Skill_Sheet_{lang.value}.pdf"
            media_type = "application/pdf"

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Template file not found: {str(e)}"
        )
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate skill sheet: {str(e)}"
        )

    return StreamingResponse(
        BytesIO(content),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/resume/preview")
async def preview_resume(
    lang: Language = Query(Language.JA, description="Skill sheet language (ja, vi, en)"),
    db: Session = Depends(get_db)
):
    """
    Preview skill sheet as HTML.

    - **lang**: Language for the skill sheet (ja=Japanese, vi=Vietnamese, en=English)

    Returns the skill sheet as HTML for preview in browser.
    """
    service = XlsxExportService(db)

    try:
        html_content = service.generate_html(lang)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Template file not found: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate preview: {str(e)}"
        )

    return HTMLResponse(content=html_content)


@router.get("/skillsheet")
async def export_skillsheet(
    lang: Language = Query(Language.JA, description="Skill sheet language (ja, vi, en)"),
    format: Literal["xlsx", "pdf", "html"] = Query("xlsx", description="Output format"),
    db: Session = Depends(get_db)
):
    """
    Generate and download skill sheet (スキルシート).

    - **lang**: Language for the skill sheet (ja=Japanese, vi=Vietnamese, en=English)
    - **format**: Output format (xlsx, pdf, html)

    Returns the skill sheet file as a download.
    """
    service = XlsxExportService(db)

    try:
        if format == "xlsx":
            content = service.generate_xlsx(lang)
            filename = f"Skill_Sheet_{lang.value}.xlsx"
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        elif format == "html":
            html_content = service.generate_html(lang)
            return HTMLResponse(content=html_content)
        else:  # pdf
            content = service.generate_pdf(lang)
            filename = f"Skill_Sheet_{lang.value}.pdf"
            media_type = "application/pdf"

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Template file not found: {str(e)}"
        )
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate skill sheet: {str(e)}"
        )

    return StreamingResponse(
        BytesIO(content),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
