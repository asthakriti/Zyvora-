from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def dashboard(
    current_user=Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "admin": current_user.email
    }