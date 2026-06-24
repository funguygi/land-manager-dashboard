from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_saved_grants
from utils.templates_v2 import page_template
from services.deadlines import deadline_sort_key

router = APIRouter()

@router.get("/calendar")
def calendar():

    grants = get_saved_grants()

    grouped = defaultdict(list)

    for g in grants:

        deadline = g[6]

        if not deadline:
            continue

        try:

            dt = deadline_sort_key(deadline)

            if dt.year > 2100:
                continue

            month_key = dt.strftime(
                "%B %Y"
            )

            grouped[month_key].append(
                (
                    dt,
                    g
                )
            )

        except:
            pass

    body = """
    <h1>Grant Calendar</h1>

    <div class="card">

    <p>
    Upcoming grant deadlines grouped by month.
    </p>

    </div>
    """

    months = sorted(
        grouped.keys(),
        key=lambda m: datetime.strptime(
            m,
            "%B %Y"
        )
    )

    for month in months:

        body += f"""
        <div class="card">

        <h2>{month}</h2>

        <table>

        <tr>
            <th>Deadline</th>
            <th>Title</th>
            <th>Agency</th>
            <th>Priority</th>
        </tr>
        """

        month_grants = sorted(
            grouped[month],
            key=lambda x: x[0]
        )

        for dt, g in month_grants:

            body += f"""
            <tr>

                <td>{g[6]}</td>

                <td>
                    <a href="/grant?url={g[0]}">
                        {g[1]}
                    </a>
                </td>

                <td>{g[3]}</td>

                <td>{g[9]}</td>

            </tr>
            """

        body += """
        </table>

        </div>
        """

    return HTMLResponse(
        page_template(
            "Calendar",
            body
        )
    )
