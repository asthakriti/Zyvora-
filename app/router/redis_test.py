from fastapi import APIRouter

from app.core.redis_client import redis_client

router = APIRouter(prefix="/redis", tags=["Redis Test"])


@router.get("/test")
def test_redis():
    redis_client.set("name", "Astha")

    value = redis_client.get("name")

    return {
        "message": "Redis is working!",
        "value": value
    }

@router.get("/hash-demo")
def redis_hash_demo():

    redis_client.hset(
        "cart:1",
        mapping={
            "product_10": 2,
            "product_20": 1,
            "product_30": 4
        }
    )

    cart = redis_client.hgetall("cart:1")

    return cart

@router.post("/cart-demo")
def cart_demo():

    redis_client.hset(
        "cart:1",
        "product_10",
        2
    )

    redis_client.hset(
        "cart:1",
        "product_20",
        5
    )

    redis_client.hset(
        "cart:1",
        "product_30",
        1
    )

    return {
        "message": "Cart stored in Redis Hash"
    }