from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.schema.cart import AddToCartRequest


def get_product_by_id(
    db: Session,
    product_id: int
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


def get_cart_by_user_id(
    db: Session,
    user_id: int
):
    return (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .first()
    )


def create_cart(
    db: Session,
    cart: Cart
):
    db.add(cart)
    db.commit()
    db.refresh(cart)

    return cart


def get_cart_item(
    db: Session,
    cart_id: int,
    product_id: int
):
    return (
        db.query(CartItem)
        .filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id
        )
        .first()
    )


def create_cart_item(
    db: Session,
    cart_item: CartItem
):
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item


def update_cart_item(
    db: Session,
    cart_item: CartItem
):
    db.commit()
    db.refresh(cart_item)

    return cart_item


def get_cart_item_by_id(
    db: Session,
    cart_id: int,
    item_id: int
):
    return (
        db.query(CartItem)
        .filter(
            CartItem.id == item_id,
            CartItem.cart_id == cart_id
        )
        .first()
    )


def delete_cart_item(
    db: Session,
    cart_item: CartItem
):
    db.delete(cart_item)
    db.commit()


def clear_cart_items(
    db: Session,
    cart_id: int
):
    (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id)
        .delete()
    )

    db.commit()