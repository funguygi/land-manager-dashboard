from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_pipeline_grants
from utils.templates_v2 import page_template
from services.deadline_alerts import deadline_flag
from database import get_tasks

router = APIRouter()

@router.get("/pipeline", response_class=HTMLResponse)
def pipeline():

    grants = get_pipeline_grants()

    interested_count = sum(
        1 for g in grants
        if g[11] == "Interested"
    )

    preparing_count = sum(
        1 for g in grants
        if g[11] == "Preparing"
    )

    submitted_count = sum(
        1 for g in grants
        if g[11] == "Submitted"
    )

    awarded_count = sum(
        1 for g in grants
        if g[11] == "Awarded"
    )

    declined_count = sum(
        1 for g in grants
        if g[11] == "Declined"
    )

    body = f"""
    <h1>Grant Pipeline</h1>

    <div class="stats">

        <div class="stat-card">
            <div class="stat-number">{interested_count}</div>
            <div class="stat-label">Interested</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{preparing_count}</div>
            <div class="stat-label">Preparing</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{submitted_count}</div>
            <div class="stat-label">Submitted</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{awarded_count}</div>
            <div class="stat-label">Awarded</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{declined_count}</div>
            <div class="stat-label">Declined</div>
        </div>

    </div>

    <div class="card">

    <table>

    <tr>
        <th>Status</th>
        <th>Score</th>
        <th>Title</th>
        <th>Agency</th>
        <th>Funding</th>
        <th>Urgency</th>
        <th>Deadline</th>
        <th>Tasks</th>
    </tr>
    """

    for g in grants:

        tasks = get_tasks(g[0])

        completed = sum(
            1 for t in tasks
            if t[2] == 1
        )

        total_tasks = len(tasks)

        progress = (
            f"{completed}/{total_tasks}"
            if total_tasks
            else "-"
        )

        status_color = {

            "Interested": "#8FB1CF",

            "Preparing": "#D7B84B",

            "Submitted": "#88A95A",

            "Awarded": "#2F4A42",

            "Declined": "#C94C4C"

        }.get(
            g[11],
            "#cccccc"
        )

        body += f"""
        <tr>

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

            <td>{g[8]}</td>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

            <td>{g[3]}</td>

            <td>{g[7]}</td>

            <td>{deadline_flag(g[6])}</td>

            <td>{g[6]}</td>

            <td>{progress}</td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Pipeline",
            body
        )
    )