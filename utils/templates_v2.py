from fastapi.responses import HTMLResponse

def page_template(title, body):

    return f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

:root {{

    --forest:#2F4A42;
    --green:#88A95A;
    --blue:#8FB1CF;
    --gold:#FFF29A;

    --glass:
        rgba(255,255,255,.78);

    --sidebar:
        rgba(255,255,255,.88);
}}

* {{
    box-sizing:border-box;
}}

body {{

    margin:0;
    padding:0;

    font-family:
        'Inter',
        sans-serif;

    background:
        linear-gradient(
            rgba(247,248,245,.15),
            rgba(247,248,245,.25)
        ),
        url('/static/background.jpg');

    background-size:cover;
    background-position:center;
    background-attachment:fixed;

    min-height:100vh;
}}

.layout {{

    display:flex;
    min-height:100vh;
}}

.sidebar {{

    width:260px;

    background:
        var(--sidebar);

    backdrop-filter:
        blur(18px);

    border-right:
        1px solid rgba(
            255,
            255,
            255,
            .5
        );

    padding:24px;

    display:flex;
    flex-direction:column;

    gap:14px;
}}

.logo {{

    width:100%;
    margin-bottom:20px;
}}

.logo img {{

    width:100%;
    height:auto;
}}

.nav-title {{

    font-size:12px;

    text-transform:uppercase;

    letter-spacing:2px;

    color:#777;

    margin-top:8px;
}}

.nav-link {{

    display:block;

    padding:14px 18px;

    border-radius:16px;

    text-decoration:none;

    color:var(--forest);

    font-weight:600;

    background:
        rgba(255,255,255,.7);

    box-shadow:
        6px 6px 14px rgba(0,0,0,.08),
        -6px -6px 14px rgba(255,255,255,.9);

    transition:.2s;
}}

.nav-link:hover {{

    transform:
        translateY(-2px);

    background:white;
}}

.main {{

    flex:1;

    padding:30px;
}}
.content-panel {{

    background:
        rgba(255,255,255,.72);

    backdrop-filter:
        blur(20px);

    border:
        1px solid rgba(
            255,
            255,
            255,
            .5
        );

    border-radius:32px;

    padding:32px;

    box-shadow:
        0 20px 50px rgba(
            0,
            0,
            0,
            .12
        );
}}

.page-header {{

    background:
        rgba(255,255,255,.55);

    backdrop-filter:
        blur(12px);

    border-radius:24px;

    padding:24px;

    margin-bottom:24px;
}}

.page-header h1 {{

    margin:0;

    color:var(--forest);

    font-size:34px;
}}

.card {{

    background:
        var(--glass);

    backdrop-filter:
        blur(16px);

    border:
        1px solid rgba(
            255,
            255,
            255,
            .5
        );

    border-radius:24px;

    padding:24px;

    margin-bottom:20px;

    box-shadow:
        0 10px 40px rgba(
            0,
            0,
            0,
            .08
        );
}}

h1,h2,h3 {{
    color:var(--forest);
}}

a {{
    color:var(--forest);
}}

@media(max-width:900px) {{

    .layout {{
        flex-direction:column;
    }}

    .sidebar {{
        width:100%;
    }}
}}

table {{

    width:100%;

    border-collapse:collapse;

    background:
        rgba(255,255,255,.45);

    border-radius:16px;

    overflow:hidden;
}}

th {{

    background:#2F4A42;

    color:white;

    padding:14px;
}}

td {{

    padding:12px;

    border-bottom:
        1px solid rgba(
            0,
            0,
            0,
            .08
        );
}}

tr:hover {{

    background:
        rgba(
            143,
            177,
            207,
            .15
        );
}}

.stats {{

    display:flex;

    gap:20px;

    flex-wrap:wrap;

    margin-bottom:24px;
}}

.stat-card {{

    flex:1;

    min-width:200px;

    border-radius:20px;

    padding:24px;

    text-align:center;

    color:white;

    box-shadow:
        0 10px 30px rgba(
            0,
            0,
            0,
            .08
        );
}}

.stat-card:nth-child(1) {{

    background:#88A95A;
}}

.stat-card:nth-child(2) {{

    background:#8FB1CF;
}}

.stat-card:nth-child(3) {{

    background:#D7B84B;
}}

.stat-card:nth-child(4) {{

    background:#2F4A42;
}}

.stat-number {{

    font-size:42px;

    font-weight:700;

    color:white;

    margin-bottom:8px;
}}

.stat-label {{

    color:white;

    opacity:.95;
}}

.card-header-green {{

    background:#88A95A;

    color:white;

    padding:18px;

    border-radius:16px;

    margin-bottom:20px;
}}

.card-header-blue {{

    background:#8FB1CF;

    color:white;

    padding:18px;

    border-radius:16px;

    margin-bottom:20px;
}}

.card-header-gold {{

    background:#D7B84B;

    color:white;

    padding:18px;

    border-radius:16px;

    margin-bottom:20px;
}}

.btn-reject {{

    background:#c94c4c;

    color:white;
}}

</style>

</head>

<body>

<div class="layout">

    <aside class="sidebar">

        <div class="logo">

            <img
                src="/static/BCLT_Logotype_Vt2.png"
                alt="Back Country Land Trust"
            >

        </div>

        <div class="nav-title">
            Navigation
        </div>

        <a class="nav-link" href="/">
            Dashboard
        </a>

        <a class="nav-link" href="/top-opportunities">
            Opportunities
        </a>

        <a class="nav-link" href="/pipeline">
            Pipeline
        </a>

        <a class="nav-link" href="/deadlines">
            Deadlines
        </a>

        <a class="nav-link" href="/calendar">
            Calendar
        </a>

        <a class="nav-link" href="/analytics">
            Analytics
        </a>

        <a class="nav-link" href="/board-report">
            Board Report
        </a>

        <a class="nav-link" href="/archived">
            Archive
        </a>

        <a class="nav-link" href="/refresh">
            Refresh
        </a>

    </aside>

    <main class="main">

        <div class="content-panel">

            {body}

        </div>

    </main>

</div>

</body>
</html>
"""