from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.cartItem import OrderItem
from app.models.cart import Cart
from app.models.user import User
from app.kafka.producer import publish_order_created


def place_order(
    db: Session,
    current_user: User
):
    try:
        cart = (
            db.query(Cart)
            .filter(Cart.user_id == current_user.id)
            .first()
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Cart not found."
            )

        if not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Cart is empty."
            )

        total_amount = 0

        for item in cart.items:

            if item.product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {item.product.name}"
                )

            total_amount += (
                item.product.price * item.quantity
            )

        order = Order(
            user_id=current_user.id,
            total_amount=total_amount
        )

        db.add(order)
        db.flush()

        for item in cart.items:

            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )

            db.add(order_item)

            item.product.stock -= item.quantity

        for item in cart.items:
            db.delete(item)

        db.commit()
        db.refresh(order)


    except Exception:
        db.rollback()
        raise

    # Database transaction is finished here

    publish_order_created(
        order_id=order.id,
        user_id=order.user_id
    )

    return order


def get_my_orders(
    db: Session,
    current_user: User
):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )


def get_order(
    db: Session,
    current_user: User,
    order_id: int
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )

    return order


def cancel_order(
    db: Session,
    current_user: User,
    order_id: int
):
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )

    if order.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled."
        )

    try:
        for item in order.order_items:
            item.product.stock += item.quantity

        order.status = "Cancelled"

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise