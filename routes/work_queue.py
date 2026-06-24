from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_saved_grants
from eligibility import evaluate_eligibility
from services.readiness import (
    calculate_readiness
)
from services.grant_priority import (
    priority_score
)
from utils.templates_v2 import page_template

router = APIRouter()

@router.get("/work-queue")
def work_queue():

    grants = get_saved_grants()

    rows = []

    for g in grants:

        eligibility = evaluate_eligibility(
            f"{g[1]} {g[10]}"
        )

        readiness = calculate_readiness(
            g,
            eligibility["status"]
        )

        priority = priority_score(
            g,
            eligibility["status"]
        )

        rows.append(
            (
                priority,
                readiness,
                g
            )
        )

    rows.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    body = """
    <h1>Work Queue</h1>

    <div class="card">

    <table>

    <tr>
        <th>Priority</th>
        <th>Readiness</th>
        <th>Grant</th>
        <th>Status</th>
    </tr>
    """

    for priority, readiness, g in rows[:25]:

        body += f"""
        <tr>

            <td>{priority}</td>

            <td>{readiness}</td>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

            <td>{g[11]}</td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Work Queue",
            body
        )
    )
