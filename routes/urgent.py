from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_saved_grants
from utils.templates_v2 import page_template
from services.deadlines import deadline_sort_value

router = APIRouter()

@router.get("/urgent", response_class=HTMLResponse)
def urgent():

    grants = get_saved_grants()

    urgent_grants = [
        g for g in grants
        if g[9] == "High"
        and g[6]
    ]

    urgent_grants.sort(
        key=lambda g:
            deadline_sort_value(g[6])
    )

    body = """
    <h1>Urgent Opportunities</h1>

    <div class="card">

    <table>

    <tr>
        <th>Score</th>
        <th>Title</th>
        <th>Agency</th>
        <th>Deadline</th>
        <th>Funding</th>
    </tr>
    """

    for g in urgent_grants:

        if g[8] >= 100:
            score_class = "score-100"

        elif g[8] >= 80:
            score_class = "score-high"

        else:
            score_class = "score-medium"

        body += f"""
        <tr>

            <td>
                <span class="{score_class}">
                    {g[8]}
                </span>
            </td>

            <td>
                <a href="/grant?url={g[0]}">
                    {g[1]}
                </a>
            </td>

            <td>{g[3]}</td>

            <td>{g[6]}</td>

            <td>{g[7]}</td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Urgent Opportunities",
            body
        )
    )
