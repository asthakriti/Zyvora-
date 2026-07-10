from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.schema.user import UserCreate

from app.service import auth_service

router = APIRouter()


@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return auth_service.signup(
        db=db,
        user=user
    )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return auth_service.login(
        db=db,
        form_data=form_data
    )


@router.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return auth_service.profile(
        current_user
    )