from datetime import UTC, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.security.dependencies import get_current_user

# Add this line to configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/users", tags=["users"])
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)
             ):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)
             ):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = User(
        email=user.email,
        name=user.name,
        password=get_password_hash(user.password),
        last_login=None
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
