from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security.config import verify_password, create_access_token


class TokenRequest(BaseModel):
    email: str
    password: str


router = APIRouter(tags=["authentication"])


@router.post("/token")
async def login(credentials: TokenRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}