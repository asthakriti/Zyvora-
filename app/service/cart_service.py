from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.schema.cart import AddToCartRequest


def add_to_cart(
    db: Session,
    current_user: User,
    request: AddToCartRequest
):
    product = db.query(Product).filter(
        Product.id == request.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == request.product_id
    ).first()

    if cart_item:
        cart_item.quantity += request.quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Product added successfully",
        "cart_item": cart_item.id
    }


def view_cart(
    db: Session,
    current_user: User
):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

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
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    cart_item.quantity = request.quantity

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Quantity updated successfully"
    }


def remove_item(
    db: Session,
    current_user: User,
    item_id: int
):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Item removed successfully"
    }


def clear_cart(
    db: Session,
    current_user: User
):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )

    db.query(CartItem).filter(
        CartItem.cart_id == cart.id
    ).delete()

    db.commit()

    return {
        "message": "Cart cleared successfully"
    }