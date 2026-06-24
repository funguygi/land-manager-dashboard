from profiles import PROFILES
from eligibility import evaluate_eligibility


def score_grant(text, profile="bclt"):

    text = (text or "").lower()

    config = PROFILES[profile]

    score = 0
    reasons = []

    # Reject rules

    for keyword in config.get(
        "reject_match",
        {}
    ):

        if keyword in text:

            return {
                "score": 0,
                "matches": [],
                "profile": profile,
                "rejected": True
            }

    # High-value matches

    for keyword, points in config[
        "high_match"
    ].items():

        if keyword in text:

            score += points
            reasons.append(keyword)

    # Low-value matches

    for keyword, penalty in config[
        "low_match"
    ].items():

        if keyword in text:

            score += penalty

    # Eligibility bonus

    eligibility = evaluate_eligibility(
        text
    )

    score += eligibility["score"]

    score = max(
        0,
        min(score, 100)
    )

    return {
        "score": score,
        "matches": reasons,
        "profile": profile,
        "eligibility": eligibility[
            "status"
        ],
        "eligibility_score": eligibility[
            "score"
        ],
        "eligibility_reasons": eligibility[
            "reasons"
        ]
    }