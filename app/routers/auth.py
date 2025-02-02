from datetime import datetime, UTC

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security.config import verify_password, create_access_token


class TokenRequest(BaseModel):
    """
    Request schema for token generation (login).

    Attributes:
        email (str): The user's email address.
        password (str): The user's password in plain text.
    """
    email: str
    password: str


# Initialize API router with tag "authentication" for grouping auth endpoints.
router = APIRouter(tags=["authentication"])


@router.post("/token")
async def login(credentials: TokenRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and generate an access token.

    This endpoint verifies the provided user credentials (email and password).
    If authentication is successful, it updates the user's last_login timestamp in the database,
    creates a JWT token for the user, and returns the token along with basic user info.

    Args:
        credentials (TokenRequest): The email and password supplied by the client.
        db (Session): The SQLAlchemy database session injected via dependency.

    Raises:
        HTTPException: If the user does not exist or the password is incorrect,
                       returns a 401 Unauthorized error.

    Returns:
        dict: A dictionary containing the access token, token type ("bearer"), and user details.
    """
    # Query the database for a user with the provided email.
    user = db.query(User).filter(User.email == credentials.email).first()

    # If user is not found or the password doesn't match, raise an Unauthorized exception.
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Update the last_login timestamp to the current UTC time.
    user.last_login = datetime.now(UTC)
    db.commit()

    # Generate a JWT access token for the authenticated user.
    access_token = create_access_token(user.email)

    # Return the token along with basic user information.
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "name": user.name,
            "last_login": user.last_login
        }
    }
