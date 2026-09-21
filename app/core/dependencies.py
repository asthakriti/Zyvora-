from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.database.connection import get_db
from app.models.user import User, UserRole
from app.repositories import user_repository


# Reads the "Authorization: Bearer <token>" header.
# tokenUrl is where Swagger's Authorize button sends the login form.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Same 401 for a bad token and for a user that no longer exists,
    # so the response does not reveal which one it was.
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    email = verify_access_token(token)

    if not email:
        raise credentials_error

    user = user_repository.get_user_by_email(
        db,
        email
    )

    if not user:
        raise credentials_error

    return user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user
