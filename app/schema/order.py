from datetime import datetime
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    order_items: list[OrderItemResponse]

    class Config:
        from_attributes = True