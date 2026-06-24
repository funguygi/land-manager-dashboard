from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from nfwf_scraper import fetch_nfwf_grants
from grantsgov_scraper import fetch_grantsgov_grants
from routes.dashboard import router as dashboard_router
from routes.metrics import router as metrics_router
from routes.pipeline import router as pipeline_router
from routes.deadlines import router as deadlines_router
from routes.grants import router as grants_router
from routes.urgent import router as urgent_router
from routes.top_opportunities import router as top_router
from routes.work_queue import (
    router as work_queue_router
)
from routes.tasks import (
    router as tasks_router
)
from routes.board_report import (
    router as board_report_router
)
from routes.pdf_report import (
    router as pdf_report_router
)
from routes.calendar import (
    router as calendar_router
)
from routes.analytics import (
    router as analytics_router
)
from routes.discovery import (
    router as discovery_router
)
from routes.archive import (
    router as archive_router
)
from parser import (
    extract_grant_info,
    extract_deadline,
    extract_funding
)
from scorer import score_grant
from scraper import fetch_ca_grants, fetch_grant_text
from metadata import set_last_refresh
from metadata import get_last_refresh
from datetime import datetime
from scheduler import start_scheduler
from services.deadline_summary import (
    deadlines_within_days
)
from services.refresh import (
    refresh_grants
)
from routes.research import (
    router as research_router
)

from routes.cleanup import (
    router as cleanup_router
)

def load_all_grants():

    return (
        fetch_ca_grants()
        + fetch_nfwf_grants()
        + fetch_grantsgov_grants()
    )

app = FastAPI()

app.include_router(dashboard_router)
app.include_router(metrics_router)
app.include_router(pipeline_router)
app.include_router(deadlines_router)
app.include_router(grants_router)
app.include_router(urgent_router)
app.include_router(top_router)
app.include_router(
    work_queue_router
)
app.include_router(tasks_router)
app.include_router(
    board_report_router
)
app.include_router(
    pdf_report_router
)
app.include_router(
    calendar_router
)
app.include_router(
    analytics_router
)
app.include_router(
    research_router
)
app.include_router(
    discovery_router
)
app.include_router(
    cleanup_router
)
app.include_router(
    archive_router
)
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

from utils.templates_v2 import page_template

from database import (
    initialize_database,
    save_grant,
    save_score,
    get_saved_grants,
    get_profile_scores,
)

initialize_database()

@app.get("/refresh")
def refresh():

    result = refresh_grants()

    return {
        "success": True,
        "processed":
            result["processed"],
        "saved":
            result["saved"]
    }

@app.on_event("startup")
def startup_event():

    start_scheduler(refresh)

@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )

@app.get("/health")
def health():

    ca = fetch_ca_grants()
    nfwf = fetch_nfwf_grants()
    grantsgov = fetch_grantsgov_grants()

    return {
        "california_grants": len(ca),
        "nfwf": len(nfwf),
        "grantsgov": len(grantsgov),

        "total_sources": 3,
        "total_opportunities":
            len(ca)
            + len(nfwf)
            + len(grantsgov)
    }
