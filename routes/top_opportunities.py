from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from database import get_saved_grants
from utils.templates_v2 import page_template

router = APIRouter()

@router.get("/top-opportunities", response_class=HTMLResponse)
def top_opportunities():

    grants = get_saved_grants()

    top = [
        g for g in grants
        if g[9] == "High"
    ]

    top.sort(
        key=lambda g: g[8],
        reverse=True
    )

    body = """
    <h1>Top Opportunities</h1>

    <div class="card">

    <table>

    <tr>
        <th>Score</th>
        <th>Title</th>
        <th>Agency</th>
        <th>Funding</th>
        <th>Deadline</th>
    </tr>
    """

    for g in top[:20]:

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

            <td>{g[7]}</td>

            <td>{g[6]}</td>

        </tr>
        """

    body += """
    </table>

    </div>
    """

    return HTMLResponse(
        page_template(
            "Top Opportunities",
            body
        )
    )
