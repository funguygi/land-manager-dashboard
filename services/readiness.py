from services.deadlines import days_until_deadline

def calculate_readiness(grant, eligibility_status):

    score = 0

    status = grant[11]

    notes = grant[10] or ""

    deadline = grant[6]

    if status == "Interested":
        score += 20

    elif status == "Preparing":
        score += 40

    elif status == "Submitted":
        score += 80

    elif status == "Awarded":
        score += 100

    if len(notes.strip()) > 25:
        score += 20

    if deadline:
        score += 10

    if eligibility_status == "Likely Eligible":
        score += 20

    elif eligibility_status == "Possibly Eligible":
        score += 10

    return min(score, 100)

def readiness_label(score):

    if score >= 80:
        return "Ready"

    if score >= 60:
        return "Active"

    if score >= 40:
        return "Planning"

    return "Not Started"
