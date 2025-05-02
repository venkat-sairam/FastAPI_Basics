

from fastapi import APIRouter
from src.db.redis.redis_client import get_redis_client as redis_client
redis_router = APIRouter()

@redis_router.get("/test")
def redis_health_check():
    
    try:
        redis = redis_client()
        redis.set("sentinel_test", "ok", ex=10)
        value = redis.get("sentinel_test")
        return {"status": "connected", "value": value}
        
    except Exception as e:
        return {"status": "Redis is down", "error": str(e)}