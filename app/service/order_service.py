from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.cartItem import OrderItem
from app.models.cart import Cart
from app.models.user import User
from app.repositories import order_repository


def place_order(
    db: Session,
    current_user: User
):
    try:
        cart = order_repository.get_cart_by_user_id(
            db,
            current_user.id
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

        # Always touch products in the same order (ascending product_id).
        # Every UPDATE takes a row lock that is held until COMMIT, so two
        # concurrent orders touching the same products in opposite orders
        # would deadlock. A deterministic order makes that impossible.
        items = sorted(
            cart.items,
            key=lambda item: item.product_id
        )

        total_amount = 0

        for item in items:

            # Fast, friendly pre-check. This is NOT the concurrency guard --
            # it only exists so the common "clearly out of stock" case fails
            # early with a readable message before we write anything.
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

        order = order_repository.create_order(
            db,
            order
        )

        for item in items:

            # AUTHORITATIVE GUARD.
            # Atomic conditional UPDATE: the stock check and the decrement
            # happen in a single SQL statement, so two concurrent orders
            # cannot both sell the last unit. rows == 0 means someone else
            # committed first between our pre-check and this write.
            rows = order_repository.decrement_stock(
                db,
                item.product_id,
                item.quantity
            )

            if rows == 0:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        f"'{item.product.name}' just went out of stock. "
                        "Please try again."
                    )
                )

            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )

            order_repository.create_order_item(
                db,
                order_item
            )

        for item in items:
            order_repository.delete_cart_item(
                db,
                item
            )

        order_repository.commit_transaction(db)

        order = order_repository.refresh_order(
            db,
            order
        )


    except Exception:
        order_repository.rollback_transaction(db)
        raise

    # Database transaction is finished here

    return order


def get_my_orders(
    db: Session,
    current_user: User
):
    return order_repository.get_orders_by_user_id(
        db,
        current_user.id
    )


def get_order(
    db: Session,
    current_user: User,
    order_id: int
):
    order = order_repository.get_order_by_id(
        db,
        current_user.id,
        order_id
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
    order = order_repository.get_order_by_id(
        db,
        current_user.id,
        order_id
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
        # Restocking is also a read-modify-write, so use the same atomic
        # statement (negative quantity = give stock back). Sorted for the
        # same deadlock reason as place_order.
        for item in sorted(
            order.order_items,
            key=lambda item: item.product_id
        ):
            order_repository.decrement_stock(
                db,
                item.product_id,
                -item.quantity
            )

        order.status = "Cancelled"

        order_repository.commit_transaction(db)

        order = order_repository.refresh_order(
            db,
            order
        )

        return order

    except Exception:
        order_repository.rollback_transaction(db)
        raise