from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=True)

    price = Column(Float, nullable=False)

    stock = Column(Integer, nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    #prduct got connected with category
    category = relationship(
        "Category",
        back_populates="products"
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    #cart_item contain the product
    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )