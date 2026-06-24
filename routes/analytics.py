from fastapi import APIRouter

from database import get_saved_grants
from services.analytics import (
    grant_metrics,
    agency_summary,
    source_summary
)

router = APIRouter()

@router.get("/summary")
def summary():

    grants = get_saved_grants()

    metrics = grant_metrics(
        grants
    )

    return {
        "total_grants":
            metrics["total_grants"],

        "high_priority":
            metrics["high_priority"],

        "medium_priority":
            metrics["medium_priority"],

        "low_priority":
            metrics["low_priority"]
    }


@router.get("/agencies")
def agencies():

    grants = get_saved_grants()

    return dict(
        agency_summary(
            grants
        )
    )


@router.get("/sources")
def sources():

    grants = get_saved_grants()

    return dict(
        source_summary(
            grants
        )
    )
