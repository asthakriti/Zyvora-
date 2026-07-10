from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schema.category import CategoryCreate


def create_category(
    db: Session,
    category: CategoryCreate
):
    existing_category = (
        db.query(Category)
        .filter(Category.name == category.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_categories(
    db: Session
):
    return db.query(Category).all()


def get_category(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryCreate
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }


def get_category_products(
    db: Session,
    category_id: int
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "category": category.name,
        "products": [
            product.name
            for product in category.products
        ]
    }