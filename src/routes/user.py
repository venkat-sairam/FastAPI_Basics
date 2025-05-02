from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session
from db.db import get_session
from db.schema import UserCreate
from db.models import User
from datetime import datetime

router = APIRouter()


@router.post("/signup")
async def signup(user: UserCreate, session: Session = Depends(get_session)):
    
    new_user = User(
        username=user.username,
        email=user.email,
        gender=user.gender,
        location=user.location,
        role=user.role,
        created_at=datetime.utcnow()
    )
    user_exists = session.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        # return {"status": "error", "status_code": 409, "message": "User already exists"}

    session.add(new_user)
    session.commit()    
    session.refresh(new_user)

    return {
            "status": "created",
            "user_id": new_user.id
        }