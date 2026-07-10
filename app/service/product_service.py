import json
import logging
import redis

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schema.product import ProductCreate
from app.schema.product import ProductResponse

from app.core.redis_client import redis_client
from app.models.product import Product

#get list of product
PRODUCTS_CACHE_KEY = "products:all"
#get_pro from id
PRODUCT_CACHE_KEY = "product:{}"
CACHE_TTL = 60  # seconds
logger = logging.getLogger(__name__)


def create_product(
    db: Session,
    product: ProductCreate
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    try:
        redis_client.delete(PRODUCTS_CACHE_KEY)
        redis_client.delete(
            PRODUCT_CACHE_KEY.format(new_product.id)
        )
    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")

    return new_product


def get_products(db: Session):
    # Check Redis first
    try:
        cached_products = redis_client.get(PRODUCTS_CACHE_KEY)

        if cached_products:
            print("========== CACHE HIT ==========")
            return json.loads(cached_products)

        print("========== CACHE MISS ==========")

    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")

    products = db.query(Product).all()

    #alchemySQL return object
    #before storing to the redis convert the object into json
    product_list = [
        ProductResponse.model_validate(product).model_dump(mode="json")
        for product in products
    ]

    try:
        redis_client.setex(
            PRODUCTS_CACHE_KEY,
            CACHE_TTL,
            json.dumps(product_list)
        )
    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")


    return product_list


def get_product(
    db: Session,
    product_id: int
):
    cache_key = PRODUCT_CACHE_KEY.format(product_id)

    try:
        cached_product = redis_client.get(cache_key)

        if cached_product:
            print("========== PRODUCT CACHE HIT ==========")
            return json.loads(cached_product)

        print("========== PRODUCT CACHE MISS ==========")

    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product_data = ProductResponse.model_validate(product).model_dump(mode="json")

    try:
        redis_client.setex(
            cache_key,
            CACHE_TTL,
            json.dumps(product_data)
        )
    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")

    return product_data


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductCreate
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    try:
        redis_client.delete(PRODUCTS_CACHE_KEY)
        redis_client.delete(
            PRODUCT_CACHE_KEY.format(product.id)
        )
    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")

    return product


def delete_product(
    db: Session,
    product_id: int
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product_id_to_delete = product.id

    db.delete(product)
    db.commit()

    try:
        redis_client.delete(PRODUCTS_CACHE_KEY)
        redis_client.delete(
            PRODUCT_CACHE_KEY.format(product_id_to_delete)
        )
    except redis.RedisError as e:
        logger.error(f"Redis Error: {e}")