from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate, PasswordChange
from app.security.config import oauth2_scheme
from app.security.dependencies import get_current_user

# Configure password hashing using bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize the API router for user-related endpoints.
router = APIRouter(prefix="/users", tags=["users"])


def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash for the given plain text password.

    Args:
        password (str): The plain text password that needs to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a list of all users.

    This endpoint is protected and requires a valid JWT token.
    It returns all users present in the database.

    Args:
        db (Session): SQLAlchemy database session provided via dependency.
        current_user (User): The currently authenticated user obtained via dependency.

    Returns:
        List[UserResponse]: A list of user details.
    """
    users = db.query(User).all()
    return users


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve information about the currently authenticated user.

    Args:
        current_user (User): The current user provided by the authentication dependency.

    Returns:
        UserResponse: The details of the currently authenticated user.
    """
    return current_user


@router.post("/password", status_code=200)
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change the current user's password.

    This endpoint accepts new password data, hashes it using bcrypt,
    updates the user's password in the database, and commits the changes.

    Args:
        password_data (PasswordChange): The new password data.
        db (Session): SQLAlchemy database session provided via dependency.
        current_user (User): The currently authenticated user.

    Returns:
        None
    """
    # Hash the new password before updating the user's record.
    new_hashed_password = get_password_hash(password_data.password)
    current_user.password = new_hashed_password
    db.commit()


@router.delete("/deletion", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete the account of the currently authenticated user.

    This endpoint removes the user's record from the database and commits the transaction.
    After deletion, a 204 No Content response is returned.

    Args:
        db (Session): SQLAlchemy database session provided via dependency.
        current_user (User): The currently authenticated user.

    Returns:
        None
    """
    db.delete(current_user)
    db.commit()
    return None


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve details of a specific user given their unique identifier.

    Args:
        user_id (int): The unique identifier of the user to retrieve.
        db (Session): SQLAlchemy database session provided via dependency.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: If the user with the given ID does not exist.

    Returns:
        UserResponse: The details of the requested user.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user in the system.

    This endpoint validates whether a user with the provided email already exists.
    If not, it creates a new user record with a hashed password and sets the last_login
    to None, then returns the created user's details.

    Args:
        user (UserCreate): The user data for registration.
        db (Session): SQLAlchemy database session provided via dependency.

    Raises:
        HTTPException: If the email is already registered (HTTP 400).

    Returns:
        UserResponse: The details of the newly created user.
    """
    # Check if there is an existing user with the same email.
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a new user instance.
    db_user = User(
        email=user.email,
        name=user.name,
        password=get_password_hash(user.password),
        last_login=None
    )

    # Add the new user to the database and commit the transaction.
    db.add(db_user)
    db.commit()
    # Refresh the instance to load any new data (e.g., generated user_id).
    db.refresh(db_user)

    return db_user
