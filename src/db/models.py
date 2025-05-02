from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from enum import Enum
from datetime import datetime
from db.schema import GenderEnum, RoleEnum
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True, index=True) 
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True, nullable=False)

    username: str = Field(max_length=32)
    email: str = Field(max_length=64, unique=True)

    gender: Optional[GenderEnum] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=64)

    role: RoleEnum = Field(default=RoleEnum.user)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": "now()"},
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": "now()", "onupdate": "now()"},
        nullable=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )
