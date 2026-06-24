ELIGIBILITY_RULES = {

    # Strong positive signals

    "501(c)(3)": 20,
    "nonprofit": 10,
    "non-profit": 10,
    "land trust": 25,
    "conservation organization": 20,
    "wildlife": 10,
    "habitat": 10,
    "restoration": 10,
    "stewardship": 10,
    "open space": 10,
    "biodiversity": 10,
    "watershed": 10,
    "riparian": 10,

    # Moderate positives

    "community organization": 5,
    "special district": 5,
    "tribe": 5,
    "tribal organization": 5,

    # Negative signals

    "local government only": -30,
    "state agency only": -40,
    "federal agency only": -40,
    "charter school": -50,
    "school district": -50,
    "university only": -40,
    "for profit only": -50,
    "tribal government only": -25,
}


def evaluate_eligibility(text):

    text = (text or "").lower()

    score = 0
    reasons = []

    for phrase, value in ELIGIBILITY_RULES.items():

        if phrase in text:

            score += value
            reasons.append(phrase)

    if score >= 40:

        status = "Likely Eligible"

    elif score >= 15:

        status = "Possibly Eligible"

    elif score <= -20:

        status = "Unlikely Eligible"

    else:

        status = "Needs Review"

    return {
        "status": status,
        "score": score,
        "reasons": reasons
    }