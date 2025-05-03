from sqlmodel import SQLModel
from typing import Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    guest = "guest"


class UserCreate(SQLModel):
    username: str
    email: str
    gender: Optional[GenderEnum] = None
    location: Optional[str] = None
    role: Optional[RoleEnum] = RoleEnum.user
