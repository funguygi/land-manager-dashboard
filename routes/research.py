from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from scorer import score_grant

from scraper import (
    fetch_ca_grants,
    fetch_grant_text
)

router = APIRouter()


@router.get("/research")
def research_grants():

    grants = fetch_ca_grants()

    results = []

    for grant in grants[:15]:

        text = fetch_grant_text(
            grant["url"]
        )

        if not text:
            continue

        score = score_grant(
            text,
            profile="research"
        )

        results.append({
            "title":
                grant["title"],

            "score":
                score["score"],

            "matches":
                score["matches"]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:20]


@router.get("/federal")
def federal():

    grants = fetch_ca_grants()

    results = []

    for grant in grants[:15]:

        text = fetch_grant_text(
            grant["url"]
        )

        if not text:
            continue

        score = score_grant(
            text,
            profile="research"
        )

        results.append({
            "title":
                grant["title"],

            "score":
                score["score"],

            "matches":
                score["matches"]
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:20]


@router.get("/why")
def why(
    url: str,
    profile="wrights_field"
):

    text = fetch_grant_text(
        url
    )

    result = score_grant(
        text,
        profile
    )

    return result


@router.get("/research-dashboard")
def research_dashboard():

    return RedirectResponse(
        "/dashboard?profile=research",
        status_code=302
    )
