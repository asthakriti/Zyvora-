from fastapi import FastAPI

import logging
import app.models.user

from app.router.auth import router as auth_router
from app.router.admin import router as admin_router
from app.models.product import Product
from app.router.product import router as product_router
from app.router.category import router as category_router
from app.models.cart import Cart, CartItem
from app.router.cart import router as cart_router
from app.router.order import router as order_router
from app.middleWare.rate_limit import rate_limit


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

app = FastAPI()

app.middleware("http")(rate_limit)

# Tables are created and changed only by Alembic migrations (alembic/versions).

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)


@app.get("/")
def home():
    return {"message": "Ecommerce Backend Running"}