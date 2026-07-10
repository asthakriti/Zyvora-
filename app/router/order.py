from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.models.user import User

from app.schema.order import OrderResponse

from app.auth.dependencies import get_current_user

from app.service import order_service


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=OrderResponse)
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.place_order(
        db=db,
        current_user=current_user
    )


@router.get("/", response_model=list[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.get_my_orders(
        db=db,
        current_user=current_user
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.get_order(
        db=db,
        current_user=current_user,
        order_id=order_id
    )


@router.patch("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.cancel_order(
        db=db,
        current_user=current_user,
        order_id=order_id
    )