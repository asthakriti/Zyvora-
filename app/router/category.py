from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schema.category import CategoryCreate, CategoryResponse
from app.auth.roles import admin_required
from app.service import category_service

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return category_service.create_category(
        db=db,
        category=category
    )


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    return category_service.get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return category_service.get_category(
        db=db,
        category_id=category_id
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return category_service.update_category(
        db=db,
        category_id=category_id,
        category_data=category_data
    )


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return category_service.delete_category(
        db=db,
        category_id=category_id
    )


@router.get("/{category_id}/products")
def get_category_products(
    category_id: int,
    db: Session = Depends(get_db)
):
    return category_service.get_category_products(
        db=db,
        category_id=category_id
    )