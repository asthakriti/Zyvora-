from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.cart import Cart
from app.models.cartItem import OrderItem


def get_cart_by_user_id(
    db: Session,
    user_id: int
):
    return (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .first()
    )


def create_order(
    db: Session,
    order: Order
):
    db.add(order)
    db.flush()

    return order


def create_order_item(
    db: Session,
    order_item: OrderItem
):
    db.add(order_item)


def delete_cart_item(
    db: Session,
    cart_item
):
    db.delete(cart_item)


def commit_transaction(db: Session):
    db.commit()


def rollback_transaction(db: Session):
    db.rollback()


def refresh_order(
    db: Session,
    order: Order
):
    db.refresh(order)
    return order


def get_orders_by_user_id(
    db: Session,
    user_id: int
):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .all()
    )


def get_order_by_id(
    db: Session,
    user_id: int,
    order_id: int
):
    return (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == user_id
        )
        .first()
    )