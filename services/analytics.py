from collections import Counter


def agency_summary(grants):

    counts = Counter()

    for g in grants:

        agency = g[3]

        if agency:
            counts[agency] += 1

    return sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )


def source_summary(grants):

    counts = Counter()

    for g in grants:

        source = g[2]

        if source:
            counts[source] += 1

    return sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )


def priority_summary(grants):

    result = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for g in grants:

        priority = g[9]

        if priority in result:
            result[priority] += 1

    return result


def application_status_summary(grants):

    counts = Counter()

    for g in grants:

        status = g[11]

        if status:
            counts[status] += 1

    return dict(counts)


def grant_metrics(grants):

    priorities = priority_summary(
        grants
    )

    statuses = application_status_summary(
        grants
    )

    return {
        "total_grants":
            len(grants),

        "high_priority":
            priorities["High"],

        "medium_priority":
            priorities["Medium"],

        "low_priority":
            priorities["Low"],

        "interested":
            statuses.get(
                "Interested",
                0
            ),

        "preparing":
            statuses.get(
                "Preparing",
                0
            ),

        "submitted":
            statuses.get(
                "Submitted",
                0
            ),

        "awarded":
            statuses.get(
                "Awarded",
                0
            ),

        "declined":
            statuses.get(
                "Declined",
                0
            )
    }
