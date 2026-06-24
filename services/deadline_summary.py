from datetime import datetime

from services.deadlines import (
    deadline_sort_key
)

def deadlines_within_days(
    grants,
    days
):

    results = []

    for g in grants:

        deadline = g[6]

        if not deadline:
            continue

        try:

            delta = (
                deadline_sort_key(deadline)
                - datetime.now()
            ).days

            if 0 <= delta <= days:

                results.append(g)

        except:
            pass

    return results
