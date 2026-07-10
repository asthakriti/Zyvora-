from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.redis_client import redis_client

MAX_REQUESTS = 1000
WINDOW = 60


async def rate_limit(request: Request, call_next):

    if request.url.path in ["/docs", "/openapi.json", "/favicon.ico"]:
        return await call_next(request)

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    requests = redis_client.get(key)

    if requests is None:
        redis_client.setex(
            key,
            WINDOW,
            1
        )

    else:
        requests = int(requests)

        if requests >= MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too Many Requests"
                }
            )

        redis_client.incr(key)

    response = await call_next(request)

    return response