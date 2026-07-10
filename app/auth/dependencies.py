from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.oauth2 import oauth2_scheme
from app.auth.jwt_handler import verify_token
from app.database.connection import get_db
from app.models.user import User

#Token -> Email -> User

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_token(token)

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user