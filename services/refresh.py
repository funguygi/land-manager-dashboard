from datetime import datetime

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

from scorer import score_grant

from database import (
    save_grant,
    save_score
)

from metadata import (
    set_last_refresh
)

from parser import (
    extract_grant_info,
    extract_deadline
)

def refresh_grants():

    grants = (
        fetch_ca_grants()
        + fetch_nfwf_grants()
        + fetch_grantsgov_grants()
    )

    saved = 0

    for grant in grants:

        try:

            text = fetch_grant_text(
                grant["url"]
            )

            if not text:
                text = grant["title"]

            result = score_grant(
                text,
                profile="bclt"
            )

            if result.get("rejected"):
                continue

            info = extract_grant_info(text)

            grant["agency"] = (
                info.get("agency")
                or grant.get("agency", "")
            )

            grant["funding"] = (
                info.get("funding")
                or grant.get("funding", "")
            )

            deadline = extract_deadline(text)

            if deadline:
                grant["deadline"] = deadline

            score = result["score"]

            save_score(
                grant["url"],
                "bclt",
                score
            )

            grant["score"] = score

            print(
                grant["title"],
                grant.get("funding"),
                grant.get("deadline")
            )

            save_grant(grant)

        except Exception as e:

            print(
                "Refresh error:",
                grant.get("title"),
                e
            )

    set_last_refresh(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
    )

    return {
        "processed": len(grants),
        "saved": saved
    }
