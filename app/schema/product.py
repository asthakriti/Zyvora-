from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    description: str
    # Matches Numeric(10, 2) in the database: more than 2 decimal places is rejected.
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal  # sent as a string, e.g. "19.99"
    stock: int
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True