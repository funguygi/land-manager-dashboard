from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from database import (
    get_saved_grants,
    get_pipeline_grants
)

router = APIRouter()

@router.get("/export-board-report")
def export_board_report():

    grants = get_saved_grants()

    pipeline = get_pipeline_grants()

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Grant Steward Board Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            f"Total Grants: {len(grants)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Pipeline Grants: {len(pipeline)}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            "Top Opportunities",
            styles["Heading2"]
        )
    )

    for g in grants[:10]:

        story.append(
            Paragraph(
                f"{g[1]} (Score {g[8]})",
                styles["Normal"]
            )
        )

    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=board_report.pdf"
        }
    )
