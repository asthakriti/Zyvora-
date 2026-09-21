from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: Decimal

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    order_items: list[OrderItemResponse]

    class Config:
        from_attributes = True