# src/dependencies/rate_limiter.py
import os
from fastapi import Header, HTTPException, status
from datetime import timedelta
from src.db.redis.redis_client import get_redis_client

def rate_limiter(
    x_user_id: str = Header(..., alias="X-User-ID"),
    x_user_role: str = Header(None, alias="X-User-Role"),  # role ignored in TEST_MODE
):
    r = get_redis_client()
    test_mode = os.getenv("TEST_MODE", "true").lower() == "true"
    if not test_mode:
        # if you ever disable TEST_MODE, you can add normal logic back here
        return

    # Test-mode settings
    limit = 3
    window = 60       # seconds
    block_secs = 30   # seconds
    usage_key = f"usage:{x_user_id}:test"   # single rolling window key
    block_key = f"blocked:{x_user_id}"

    # 1️⃣ If already blocked, reject
    if r.exists(block_key):
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Temporarily blocked. Try again later."
        )

    # 2️⃣ Increment and expire usage counter
    count = r.incr(usage_key)
    if count == 1:
        r.expire(usage_key, window)

    # 3️⃣ On exceeding limit, set block and reject
    if count > limit:
        r.setex(block_key, timedelta(seconds=block_secs), "1")
        raise HTTPException(
            status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded ({limit}/{window}s). Blocked for {block_secs}s."
        )

    # ✅ Otherwise allow through
    return
