from services.readiness import calculate_readiness

def priority_score(grant, eligibility_status):

    readiness = calculate_readiness(
        grant,
        eligibility_status
    )

    grant_score = grant[8]

    total = (
        grant_score * 0.6
        + readiness * 0.4
    )

    return round(total, 1)
