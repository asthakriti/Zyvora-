from fastapi import FastAPI

from app.database.connection import engine
from app.database.base import Base
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
from app.router import redis_test
from app.middleWare.rate_limit import rate_limit
from app.router.session_demo import router as session_router


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

app = FastAPI()

app.middleware("http")(rate_limit)


print("APP ID:", id(app))

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(redis_test.router)
app.include_router(session_router)

for route in app.routes:
    print(route.path)

@app.get("/")
def home():
    return {"message": "Ecommerce Backend Running"}