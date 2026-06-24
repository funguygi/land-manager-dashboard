from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import (
    get_saved_grants,
    get_pipeline_grants
)

from utils.templates_v2 import page_template

from services.funding import (
    total_funding,
    format_currency
)

from services.deadline_summary import (
    deadlines_within_days
)

router = APIRouter()

@router.get("/board-report")
def board_report():

    grants = get_saved_grants()

    pipeline = get_pipeline_grants()

    total_grants = len(grants)

    total_pipeline = len(pipeline)

    high_priority = sum(
        1 for g in grants
        if g[9] == "High"
    )

    interested = sum(
        1 for g in grants
        if g[11] == "Interested"
    )

    preparing = sum(
        1 for g in grants
        if g[11] == "Preparing"
    )

    submitted = sum(
        1 for g in grants
        if g[11] == "Submitted"
    )

    awarded = sum(
        1 for g in grants
        if g[11] == "Awarded"
    )

    funding_total = total_funding(
        grants
    )

    due_30 = deadlines_within_days(
        grants,
        30
    )

    body = f"""
    <h1>Board Report</h1>

    <div class="stats">

        <div class="stat-card">
            <div class="stat-number">{total_grants}</div>
            <div class="stat-label">Total Grants</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{high_priority}</div>
            <div class="stat-label">High Priority</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{total_pipeline}</div>
            <div class="stat-label">Pipeline</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">
                {format_currency(funding_total)}
            </div>
            <div class="stat-label">
                Potential Funding
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-number">
                {len(due_30)}
            </div>
            <div class="stat-label">
                Due Within 30 Days
            </div>
        </div>

    </div>

    <div class="card">

    <h2>Application Status</h2>

    <ul>
        <li>Interested: {interested}</li>
        <li>Preparing: {preparing}</li>
        <li>Submitted: {submitted}</li>
        <li>Awarded: {awarded}</li>
    </ul>

    </div>

    <div class="card">

    <h2>Upcoming Deadlines (30 Days)</h2>

    <table>

    <tr>
        <th>Title</th>
        <th>Agency</th>
        <th>Deadline</th>
    </tr>
    """

    for g in due_30[:10]:

        body += f"""
        <tr>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

            <td>{g[3]}</td>

            <td>{g[6]}</td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Board Report",
            body
        )
    )
