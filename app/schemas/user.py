from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    password: str
    is_active: bool = True


class UserCreate(UserBase):
    # Inherits all fields from UserBase and adds none
    last_login: Optional[datetime] = None
    # Contains:
    # - email: str
    # - name: str
    # - password: str


class UserResponse(UserBase):
    # Inherits all fields from UserBase and adds:
    user_id: int
    created_at: datetime
    last_login: Optional[datetime]

    # Contains:
    # - email: str
    # - name: str
    # - password: str
    # - is_active: bool
    # - user_id: int
    # - created_at: datetime
    # - last_login: Optional[datetime]
