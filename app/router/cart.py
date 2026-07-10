from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
from app.schema.cart import AddToCartRequest

from app.service import cart_service

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post("/add")
def add_to_cart(
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.add_to_cart(
        db=db,
        current_user=current_user,
        request=request
    )


@router.get("")
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.view_cart(
        db=db,
        current_user=current_user
    )


@router.put("/item/{item_id}")
def update_quantity(
    item_id: int,
    request: AddToCartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.update_quantity(
        db=db,
        current_user=current_user,
        item_id=item_id,
        request=request
    )


@router.delete("/item/{item_id}")
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.remove_item(
        db=db,
        current_user=current_user,
        item_id=item_id
    )


@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return cart_service.clear_cart(
        db=db,
        current_user=current_user
    )