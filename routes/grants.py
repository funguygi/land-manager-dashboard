from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from database import (
    get_grant,
    update_notes,
    update_application_status
)

from eligibility import evaluate_eligibility
from services.checklists import generate_checklist
from services.deadlines import days_until_deadline
from utils.templates_v2 import page_template
from services.readiness import (
    calculate_readiness,
    readiness_label
)
from database import (
    save_task,
    get_tasks
)

router = APIRouter()

@router.get("/update-status")
def update_status(url: str, status: str):

    update_application_status(
        url,
        status
    )

    return RedirectResponse(
        f"/grant?url={url}",
        status_code=302
    )

@router.get("/update-notes")
def update_grant_notes(url: str, notes: str):

    update_notes(url, notes)

    return RedirectResponse(
        f"/grant?url={url}",
        status_code=302
    )

@router.get("/grant", response_class=HTMLResponse)
def grant_detail(url: str):

    g = get_grant(url)

    if not g:
        return HTMLResponse(
            "<h2>Grant not found</h2>"
        )

    eligibility = evaluate_eligibility(
        f"""
        {g[1]}
        {g[3]}
        {g[10]}
        """
    )

    readiness_score = calculate_readiness(
        g,
        eligibility["status"]
    )

    readiness_status = readiness_label(
        readiness_score
    )

    checklist = generate_checklist(
        f"""
        {g[1]}
        {g[10]}
        """
    )

    for task in checklist:

        save_task(
            g[0],
            task
        )

    stored_tasks = get_tasks(
        g[0]
    )

    checklist_html = ""

    for task_id, task_name, completed in stored_tasks:

        symbol = "☑" if completed else "□"

        checklist_html += f"""
        <li>

            <a href="/toggle-task?task_id={task_id}&url={g[0]}">

                {symbol}

            </a>

            {task_name}

        </li>
        """

    body = f"""
    <h1>{g[1]}</h1>

    <div class="card">

    <h3>Grant Summary</h3>

    <p><b>Agency:</b> {g[3]}</p>

    <p><b>Status:</b> {g[4]}</p>

    <p><b>Open Date:</b> {g[5]}</p>

    <p><b>Deadline:</b> {g[6]}</p>

    <p><b>Time Remaining:</b>
        {days_until_deadline(g[6])}
    </p>

    <p><b>Funding:</b> {g[7]}</p>

    <p><b>Score:</b> {g[8]}</p>

    <p><b>Priority:</b> {g[9]}</p>

    <p><b>Application Status:</b> {g[11]}</p>

    </div>

    <div class="card">

    <h3>Eligibility Analysis</h3>

    <p>
        <b>Status:</b>
        {eligibility["status"]}
    </p>

    <p>
        <b>Reasons:</b>
        {", ".join(eligibility["reasons"])}
    </p>

    </div>

    <div class="card">

        <div class="card">

    <h3>Grant Readiness</h3>

    <p>
        <b>Score:</b>
        {readiness_score}/100
    </p>

    <p>
        <b>Status:</b>
        {readiness_status}
    </p>

    </div>

    <h3>Application Checklist</h3>

    <ul>

    {checklist_html}

    </ul>

    </div>

    <div class="card">

    <h3>Application Actions</h3>

    <a class="action-button btn-interested"
    href="/update-status?url={g[0]}&status=Interested">
    Interested
    </a>

    <a class="action-button btn-preparing"
    href="/update-status?url={g[0]}&status=Preparing">
    Preparing
    </a>

    <a class="action-button btn-submitted"
    href="/update-status?url={g[0]}&status=Submitted">
    Submitted
    </a>

    <a class="action-button btn-awarded"
    href="/update-status?url={g[0]}&status=Awarded">
    Awarded
    </a>

    <a class="action-button btn-declined"
    href="/update-status?url={g[0]}&status=Declined">
    Declined
    </a>

    <a class="action-button"
    href="/archive-grant?url={g[0]}">
    Archive
    </a>

    <a class="action-button btn-declined"
    href="/reject-grant?url={g[0]}"
    onclick="return confirm('Remove this grant permanently?');">
    Not Relevant
    </a>

    </div>

    <div class="card">

    <h3>Notes</h3>

    <form action="/update-notes">

        <input
            type="hidden"
            name="url"
            value="{g[0]}"
        >

        <textarea
            name="notes"
            rows="10"
            cols="100"
        >{g[10]}</textarea>

        <br><br>

        <button type="submit">
            Save Notes
        </button>

    </form>

    </div>

    <div class="card">

    <p>
        <a href="{g[0]}" target="_blank">
            Open Original Grant
        </a>
    </p>

    <p>
        <a href="/dashboard">
            Back to Dashboard
        </a>
    </p>

    </div>
    """

    return HTMLResponse(
        page_template(
            g[1],
            body
        )
    )
