from sqlalchemy.orm import Session

from app.models.category import Category
from app.schema.category import CategoryCreate


def get_category_by_name(
    db: Session,
    category_name: str
):
    return (
        db.query(Category)
        .filter(Category.name == category_name)
        .first()
    )


def create_category(
    db: Session,
    category: Category
):
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(
    db: Session,
    category_id: int
):
    return (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )


def update_category(
    db: Session,
    category: Category,
    category_data: CategoryCreate
):
    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category: Category
):
    db.delete(category)
    db.commit()