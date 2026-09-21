from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)
from app.models.user import User
from app.schema.user import TokenResponse, UserCreate
from app.repositories import user_repository


def signup(
    db: Session,
    user: UserCreate
) -> User:
    existing_user = user_repository.get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    return user_repository.create_user(
        db,
        new_user
    )


def login(
    db: Session,
    email: str,
    password: str
) -> TokenResponse:
    db_user = user_repository.get_user_by_email(
        db,
        email
    )

    # One message for both cases, so the response does not
    # reveal whether an email is registered.
    if not db_user or not verify_password(
        password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(
        subject=db_user.email
    )

    return TokenResponse(access_token=token)
