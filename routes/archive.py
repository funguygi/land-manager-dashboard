from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from database import (
    archive_old_grants,
    get_archived_grants,
    restore_grant,
    archive_grant
)
from database import (
    archive_old_grants,
    get_archived_grants,
    restore_grant
)
from database import (
    archive_old_grants,
    get_archived_grants,
    restore_grant,
    archive_grant,
    delete_grant
)

router = APIRouter()

@router.get("/archive-grant")
def archive_grant_route(url: str):

    archive_grant(url)

    return RedirectResponse(
        "/dashboard",
        status_code=302
    )

@router.get("/archive")
def archive():

    archive_old_grants()

    return {
        "success": True,
        "message": "Old grants archived"
    }


@router.get("/archived")
def archived():

    return get_archived_grants()


@router.get("/restore")
def restore(url: str):

    restore_grant(url)

    return RedirectResponse(
        "/archived",
        status_code=302
    )

@router.get("/reject-grant")
def reject_grant(url: str):

    delete_grant(url)

    return RedirectResponse(
        "/dashboard",
        status_code=302
    )