from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.cart import Cart
from app.models.cartItem import OrderItem
from app.models.product import Product


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


def decrement_stock(
    db: Session,
    product_id: int,
    quantity: int
) -> int:
    """
    Atomically decrement product stock.

    Emits a single statement:

        UPDATE products
        SET    stock = stock - :quantity
        WHERE  id = :product_id
          AND  stock >= :quantity

    The check (`stock >= quantity`) and the write (`stock - quantity`) happen
    inside ONE statement, so no other transaction can slip in between them.
    `stock - quantity` is evaluated by PostgreSQL at write time, not by Python
    from a value read earlier -- that is what prevents the lost update.

    Returns the number of rows updated:
        1 -> stock was sufficient and has been reserved
        0 -> not enough stock (someone else took it first)
    """
    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.stock >= quantity
        )
        .update(
            {Product.stock: Product.stock - quantity},
            synchronize_session=False
        )
    )


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