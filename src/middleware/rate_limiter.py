# src/dependencies/rate_limiter.py

from fastapi import Header, HTTPException, status
from datetime import timedelta, datetime, timezone
from src.db.redis.redis_client import get_redis_client
from src.utils.redis_keys import get_hour_key, get_day_key, get_block_key, get_role_limit_key

def rate_limiter(
    x_user_id: str = Header(..., alias="X-User-ID"),
    x_user_role: str = Header(..., alias="X-User-Role"),
):
    r = get_redis_client()

    # Block check
    block_key = get_block_key(x_user_id)
    if r.exists(block_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You are temporarily blocked due to too many requests on the endpoint."
        )

    #  Load role‐based limits
    rl = r.hgetall(get_role_limit_key(x_user_role))
    if not rl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    hourly_limit = int(rl.get("hour", 100))
    daily_limit  = int(rl.get("day", 1000))

    # 3️⃣ Increment per‐hour and per‐day counters
    now = datetime.now(timezone.utc)
    hour_key = get_hour_key(x_user_id)
    day_key  = get_day_key(x_user_id)

    h = r.incr(hour_key)
    if h == 1:
        r.expire(hour_key, 3600)

    d = r.incr(day_key)
    if d == 1:
        r.expire(day_key, 86400)

    # 4️⃣ Enforce thresholds
    if h > hourly_limit or d > daily_limit:
        r.setex(block_key, timedelta(hours=3), "1")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Blocked for 3 hours."
        )

    return  # allowed through
