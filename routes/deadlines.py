from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_active_grants
from alerts import deadline_alert
from utils.templates_v2 import page_template

router = APIRouter()

from services.deadlines import (
    days_until_deadline,
    deadline_sort_key
)
from services.deadline_alerts import deadline_flag

@router.get("/deadlines", response_class=HTMLResponse)
def deadlines():

    grants = get_active_grants()

    grants.sort(
        key=lambda g: deadline_sort_key(g[6])
    )

    urgent = sum(
        1 for g in grants
        if deadline_flag(g[6]) == "🔥"
    )

    warning = sum(
        1 for g in grants
        if deadline_flag(g[6]) == "⚠"
    )

    safe = sum(
        1 for g in grants
        if deadline_flag(g[6]) == "✓"
    )

    body = f"""
    <h1>Upcoming Deadlines</h1>

    <div class="stats">

        <div class="stat-card">
            <div class="stat-number">{urgent}</div>
            <div class="stat-label">Critical</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{warning}</div>
            <div class="stat-label">Upcoming</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{safe}</div>
            <div class="stat-label">Safe</div>
        </div>

    </div>

    <div class="card">
   
    <table>

    <tr>
        <th>Risk</th>
        <th>Opportunity</th>
        <th>Status</th>
        <th>Countdown</th>
        <th>Deadline</th>
        <th>Funding</th>
        <th>Title</th>
    </tr>
    """

    for g in grants:

        countdown = days_until_deadline(g[6])

        status_color = {

            "Interested": "#8FB1CF",

            "Preparing": "#D7B84B",

            "Submitted": "#88A95A",

            "Awarded": "#2F4A42"

        }.get(
            g[11],
            "#cccccc"
        )

        body += f"""
        <tr>

            <td>{deadline_flag(g[6])}</td>

            <td>

                <span style="
                    background:{status_color};
                    color:white;
                    padding:6px 12px;
                    border-radius:12px;
                    font-weight:bold;
                ">
                    {g[11]}
                </span>

            </td>

            <td>{countdown}</td>

            <td>{g[6]}</td>

            <td>{g[7]}</td>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Deadlines",
            body
        )
    )