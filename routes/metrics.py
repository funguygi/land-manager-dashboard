from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_saved_grants
from utils.templates_v2 import page_template

router = APIRouter()

@router.get("/metrics", response_class=HTMLResponse)
def metrics():

    grants = get_saved_grants()

    total = len(grants)

    high = sum(
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

    declined = sum(
        1 for g in grants
        if g[11] == "Declined"
    )

    agencies = len(
        set(
            g[3]
            for g in grants
            if g[3]
        )
    )

    body = f"""
    <h1>Grant Steward Metrics</h1>

    <div class="stats">

        <div class="stat-card">
            <div class="stat-number">{total}</div>
            <div class="stat-label">Total Grants</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{high}</div>
            <div class="stat-label">High Priority</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">{agencies}</div>
            <div class="stat-label">Agencies</div>
        </div>

    </div>

    <div class="card">

        <h2>Pipeline</h2>

        <p><b>Interested:</b> {interested}</p>
        <p><b>Preparing:</b> {preparing}</p>
        <p><b>Submitted:</b> {submitted}</p>
        <p><b>Awarded:</b> {awarded}</p>
        <p><b>Declined:</b> {declined}</p>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Metrics",
            body
        )
    )