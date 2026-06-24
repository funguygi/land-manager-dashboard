from fastapi.responses import HTMLResponse

def page_template(title, body):

    return f"""
    <html>

    <head>

    <title>{title}</title>

    <style>

    body {{
        font-family: Arial, sans-serif;
        max-width: 1400px;
        margin: auto;
        padding: 20px;
        background: #f4f7f4;
        color: #333;
    }}

    h1 {{
        color: #2f5d3a;
    }}

    .navbar {{
        background: #2f5d3a;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
    }}

    .navbar a {{
        color: white;
        text-decoration: none;
        margin-right: 15px;
        font-weight: bold;
    }}

    .navbar a:hover {{
        text-decoration: underline;
    }}

    .card {{
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,.1);
        margin-bottom: 15px;
    }}

    .stats {{
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }}

    .stat-card {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,.1);
        min-width: 180px;
        text-align: center;
    }}

    .stat-number {{
        font-size: 32px;
        font-weight: bold;
        color: #2f5d3a;
    }}

    .stat-label {{
        color: #666;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
    }}

    th {{
        background: #2f5d3a;
        color: white;
    }}

    th, td {{
        padding: 10px;
        border: 1px solid #ddd;
        text-align: left;
    }}

    tr:nth-child(even) {{
        background: #f8f8f8;
    }}

    </style>

    </head>

    <body>

    <div class="navbar">

        <a href="/">🌿 Grant Steward</a>
        <a href="/dashboard">Dashboard</a>
        <a href="/pipeline">Pipeline</a>
        <a href="/deadlines">Deadlines</a>
        <a href="/calendar">Calendar</a>
        <a href="/urgent">Urgent</a>
        <a href="/top-opportunities">Top Opportunities</a>
        <a href="/metrics">Metrics</a>
        <a href="/work-queue">Work Queue</a>
        <a href="/board-report">Board Report</a>
        <a href="/export-board-report">PDF Report</a>
        <a href="/calendar">Calendar</a>
        <a href="/refresh">Refresh</a>

    </div>

    {body}

    </body>

    </html>
    """