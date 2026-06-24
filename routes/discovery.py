from fastapi import APIRouter

from scorer import score_grant

from scraper import (
    fetch_grant_text
)

from database import (
    save_score,
    get_saved_grants
)

from scraper import (
    fetch_ca_grants,
    fetch_grant_text
)

from nfwf_scraper import (
    fetch_nfwf_grants
)

from grantsgov_scraper import (
    fetch_grantsgov_grants
)

router = APIRouter()

def load_all_grants():

    return (
        fetch_ca_grants()
        + fetch_nfwf_grants()
        + fetch_grantsgov_grants()
    )

@router.get("/search")
def search(
    profile="wrights_field"
):

    grants = load_all_grants()

    results = []

    for grant in grants[:15]:

        text = fetch_grant_text(
            grant["url"]
        )

        if not text:
            continue

        score = score_grant(
            text,
            profile=profile
        )

        save_score(
            grant["url"],
            profile,
            score["score"]
        )

        results.append({
            "title":
                grant["title"],

            "url":
                grant["url"],

            "score":
                score["score"],

            "matches":
                score["matches"],

            "profile":
                profile
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


@router.get("/saved")
def saved():

    return get_saved_grants()
