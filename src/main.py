
from fastapi import FastAPI
from src.db.db import init_db
from src.routes.user import router as user_router
app = FastAPI()

@app.on_event("startup")
def on_startup():
    print(f"{'>>' * 20} Startup event {'<<' * 20}")
    print("Initializing database...")
    init_db()
    print(f"{'>>' * 20} Database initialized {'<<' * 20}")


@app.get("/")
def health_check():
    """Health check endpoint"""
    print(f"{'>>' * 20} Health check {'<<' * 20}")
    print("Health check endpoint called")
    print(f"{'>>' * 20} Health check {'<<' * 20}")
    return {"status": "ok"}
    
app.include_router(user_router)