from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.schema.cart import AddToCartRequest
from app.repositories import cart_repository


def add_to_cart(
    db: Session,
    current_user: User,
    request: AddToCartRequest
):
    product = cart_repository.get_product_by_id(
        db,
        request.product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart = cart_repository.get_cart_by_user_id(
        db,
        current_user.id
    )

    cart = cart_repository.create_cart(
        db,
        cart
    )

    cart_item = cart_repository.get_cart_item(
        db,
        cart.id,
        request.product_id
    )

    if cart_item:
        cart_item.quantity += request.quantity
        cart_repository.update_cart_item(db, cart_item)
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        cart_item = cart_repository.create_cart_item(db, cart_item)

    return {
        "message": "Product added successfully",
        "cart_item": cart_item.id
    }


def view_cart(
    db: Session,
    current_user: User
):
    cart = cart_repository.get_cart_by_user_id(
        db,
        current_user.id
    )
    if not cart:
        return {
            "message": "Cart is empty"
        }

    items = []

    total = 0

    for item in cart.items:

        subtotal = item.quantity * item.product.price

        total += subtotal

        items.append({
            "cart_item_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "cart_id": cart.id,
        "items": items,
        "total": total
    }

def update_quantity(
    db: Session,
    current_user: User,
    item_id: int,
    request: AddToCartRequest
):
    cart = cart_repository.get_cart_by_user_id(
        db,
        current_user.id
    )

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = cart_repository.get_cart_item_by_id(
        db,
        cart.id,
        item_id
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = request.quantity

    cart_item = cart_repository.update_cart_item(
        db,
        cart_item
    )

    return {
        "message": "Quantity updated successfully"
    }


def remove_item(
    db: Session,
    current_user: User,
    item_id: int
):
    cart = cart_repository.get_cart_by_user_id(
        db,
        current_user.id
    )

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = cart_repository.get_cart_item_by_id(
        db,
        cart.id,
        item_id
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_repository.delete_cart_item(
        db,
        cart_item
    )

    return {
        "message": "Item removed successfully"
    }


def clear_cart(
    db: Session,
    current_user: User
):
    cart = cart_repository.get_cart_by_user_id(
        db,
        current_user.id
    )

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_repository.clear_cart_items(
        db,
        cart.id
    )

    return {
        "message": "Cart cleared successfully"
    }