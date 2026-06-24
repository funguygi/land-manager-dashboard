from fastapi import APIRouter

from database import (
    delete_old_grants
)

router = APIRouter()


@router.get("/cleanup")
def cleanup():

    delete_old_grants()

    return {
        "success": True,
        "message": "Old grants removed"
    }
