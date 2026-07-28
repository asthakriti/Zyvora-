from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schema.category import CategoryCreate
from app.repositories import category_repository


def create_category(
    db: Session,
    category: CategoryCreate
):
    existing_category = category_repository.get_category_by_name(
        db,
        category.name
    )

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        name=category.name
    )

    new_category = category_repository.create_category(
        db,
        new_category
    )

    return new_category


def get_categories(
    db: Session
):
    return category_repository.get_all_categories(db)

def get_category(
    db: Session,
    category_id: int
):
    category = category_repository.get_category_by_id(
        db,
        category_id
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
    category = category_repository.get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category = category_repository.update_category(
        db,
        category,
        category_data
    )

    return category


def delete_category(
    db: Session,
    category_id: int
):
    category = category_repository.get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category_repository.delete_category(
        db,
        category
    )

    return {
        "message": "Category deleted successfully"
    }


def get_category_products(
    db: Session,
    category_id: int
):
    category = category_repository.get_category_by_id(
        db,
        category_id
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