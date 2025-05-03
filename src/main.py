
from fastapi import FastAPI
from src.db.db import init_db
from src.routes.user import router as user_router
# from src.middleware.rate_limiter import RateLimiterMiddleware
from test.routes import redis_router
from src.db.redis.seed import seed_role_limits
app = FastAPI()

# app.add_middleware(RateLimiterMiddleware)

@app.on_event("startup")
def on_startup():
    print(f"{'>>' * 20} Startup event {'<<' * 20}")
    print("Initializing database...")
    init_db()
    seed_role_limits()
    print(f"{'>>' * 20} Database initialized {'<<' * 20}")

@app.get("/protected")
def protected_route():
    return {"message": "You are within the limit"}


@app.get("/")
def health_check():
    """Health check endpoint"""
    print(f"{'>>' * 20} Health check {'<<' * 20}")
    print("Health check endpoint called")
    print(f"{'>>' * 20} Health check {'<<' * 20}")
    return {"status": "ok"}
    
app.include_router(user_router)
app.include_router(redis_router, prefix="/redis", tags=["redis"])
