from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import (
    get_profile_scores,
    opportunity_score
)
from metadata import get_last_refresh
from utils.templates_v2 import page_template
from eligibility import evaluate_eligibility
from services.deadline_alerts import deadline_flag

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    grants = sorted(
        get_profile_scores("bclt"),
        key=opportunity_score,
        reverse=True
    )

    last_refresh = get_last_refresh()

    top_grants = grants[:5]

    top_html = """
    <div class="card">
    <h3>Top Opportunities</h3>
    <ul>
    """

    for g in top_grants:

        eligibility = evaluate_eligibility(
            f"""
            {g[1]}
            {g[3]}
            {g[10]}
            """
        )

        top_html += f"""
        <li>

            <a href="/grant?url={g[0]}">
                <b>{g[1]}</b>
            </a>

            <br>

            Opportunity: {opportunity_score(g)}
            |
            {eligibility["status"]}
            |
            {g[7] if len(g) > 7 else ""}
            |
            {
                f"{deadline_flag(g[6])} {g[6]}"
                if len(g) > 6 and g[6]
                else "No deadline listed"
            }

            <br><br>

            <a href="/update-status?url={g[0]}&status=Interested">
                Interested
            </a>

            |

            <a href="/update-status?url={g[0]}&status=Preparing">
                Preparing
            </a>

            |

            <a href="/archive-grant?url={g[0]}">
                Archive
            </a>

        </li>

        <br>
        """

    top_html += """
    </ul>
    </div>
    """

    stats = f"""
    <div class="stats">

        <div class="stat-card">
            <div class="stat-number">{len(grants)}</div>
            <div class="stat-label">Active Grants</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">
                {sum(1 for g in grants if len(g) > 8 and str(g[8]).isdigit() and int(g[8]) >= 80)}
            </div>
            <div class="stat-label">High Match</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">
                {sum(1 for g in grants if len(g) > 6 and g[6])}
            </div>
            <div class="stat-label">Deadlines Listed</div>
        </div>

        <div class="stat-card">
            <div class="stat-number">BCLT</div>
            <div class="stat-label">Organization</div>
        </div>

    </div>
    """

    body = f"""
    <h1>Grant Steward Dashboard</h1>

    <p>
        <b>Last Refresh:</b>
        {last_refresh}
    </p>

    <div class="card-header-green">
        <h3>Back Country Land Trust</h3>
        <p>Wright's Field Conservation Funding Dashboard</p>
    </div>

    {stats}

    {top_html}

    <table>

        <tr>
            <th>Score</th>
            <th>Opportunity</th>
            <th>Eligibility</th>
            <th>Title</th>
            <th>Agency</th>
            <th>Funding</th>
            <th>Status</th>
            <th>Deadline</th>
        </tr>
    """

    for g in grants:

        print(
            g[1],
            "| funding =", g[7],
            "| opp =", opportunity_score(g)
        )

        eligibility = evaluate_eligibility(
            f"""
            {g[1]}
            {g[3]}
            {g[10]}
            """
        )

        body += f"""
        <tr>

            <td>{g[8]}</td>

            <td>{opportunity_score(g)}</td>

            <td>{eligibility["status"]}</td>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

            <td>{g[3] if len(g) > 3 else ""}</td>

            <td>{g[7] if len(g) > 7 else ""}</td>

            <td>{deadline_flag(g[6])}</td>

            <td>{g[6] if len(g) > 6 else ""}</td>

        </tr>
        """

    body += "</table>"

    return HTMLResponse(
        page_template(
            "Dashboard",
            body
        )
    )
