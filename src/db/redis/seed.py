
# src/db/redis/seed.py

from src.db.redis.redis_client import get_redis_client
from src.utils.redis_keys import get_role_limit_key
from src.utils.redis_role_limits import DEFAULT_ROLE_LIMITS

def seed_role_limits():
    redis_client = get_redis_client()
    for role, limits in DEFAULT_ROLE_LIMITS.items():
        key = get_role_limit_key(role)
        
        if not redis_client.exists(key):
            redis_client.hset(key, mapping={ "hour": limits["hour"], "day": limits["day"] })
