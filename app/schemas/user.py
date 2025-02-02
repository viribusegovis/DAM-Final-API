from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Base model for User that contains the common fields used for both creating and retrieving a user.

    Attributes:
        email (str): The user's email address.
        name (str): The user's full name.
        password (str): The user's password (typically hashed).
        is_active (bool): Indicates whether the user account is active.
    """
    email: str
    name: str
    password: str
    is_active: bool = True


class UserCreate(UserBase):
    """
    Model for creating a new user account.

    Inherits all fields from UserBase and includes an optional last_login field.

    Attributes:
        last_login (Optional[datetime]): The timestamp of the user's last login; defaults to None.
    """
    last_login: Optional[datetime] = None
    # This model contains:
    # - email: str
    # - name: str
    # - password: str
    # - is_active: bool (default True)
    # - last_login: Optional[datetime]


class UserResponse(UserBase):
    """
    Model for returning user details from API responses.

    Inherits all fields from UserBase and adds additional read-only fields including user_id, created_at,
    and last_login.

    Attributes:
        user_id (int): The unique identifier of the user.
        created_at (datetime): The timestamp when the user account was created.
        last_login (Optional[datetime]): The timestamp of the user's last login.
    """
    user_id: int
    created_at: datetime
    last_login: Optional[datetime]
    # This model contains:
    # - email: str
    # - name: str
    # - password: str
    # - is_active: bool
    # - user_id: int
    # - created_at: datetime
    # - last_login: Optional[datetime]


class PasswordChange(BaseModel):
    """
    Model for changing a user's password.

    Attributes:
        password (str): The new password to be set for the user.
    """
    password: str
