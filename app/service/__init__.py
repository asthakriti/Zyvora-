from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schema.product import ProductCreate, ProductResponse
from app.auth.roles import admin_required
from app.service import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return product_service.create_product(
        db=db,
        product=product
    )


@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return product_service.get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return product_service.get_product(
        db=db,
        product_id=product_id
    )


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return product_service.update_product(
        db=db,
        product_id=product_id,
        product_data=product_data
    )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return product_service.delete_product(
        db=db,
        product_id=product_id
    )