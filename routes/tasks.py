from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from database import toggle_task

router = APIRouter()

@router.get("/toggle-task")
def toggle(task_id: int, url: str):

    toggle_task(task_id)

    return RedirectResponse(
        f"/grant?url={url}",
        status_code=302
    )
