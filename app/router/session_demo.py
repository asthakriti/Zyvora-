from fastapi import APIRouter
from app.core.redis_client import redis_client

router = APIRouter(
    prefix="/session",
    tags=["Redis Session Demo"]
)


@router.post("/login")
def login():

    session_id = "session_123"

    redis_client.setex(
        session_id,
        1800,
        "Astha"
    )

    return {
        "message": "Session Created",
        "session_id": session_id
    }


@router.get("/{session_id}")
def get_session(session_id: str):

    user = redis_client.get(session_id)

    if not user:
        return {
            "message": "Session Expired"
        }

    return {
        "user": user
    }


@router.delete("/{session_id}")
def logout(session_id: str):

    redis_client.delete(session_id)

    return {
        "message": "Session Deleted"
    }