from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)