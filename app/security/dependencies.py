from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security.config import SECRET_KEY, ALGORITHM

# Dependency for OAuth2 token extraction.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the JWT token supplied in the request.

    This function decodes the provided JWT token using the configured secret key and algorithm.
    It then extracts the user's email (stored under the "sub" claim) from the token payload.
    If the token is invalid or the user is not found in the database, a 401 Unauthorized exception is raised.

    Parameters:
        token (str): The JWT token extracted via OAuth2PasswordBearer dependency.
        db (Session): The SQLAlchemy database session, provided by the get_db dependency.

    Returns:
        User: The user object corresponding to the token's subject email.

    Raises:
        HTTPException: If token decoding fails, the "sub" claim is missing,
                       or the user is not found in the database.
    """
    # Define an exception to be raised for any authentication issues.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        # Decode the JWT token using the configured SECRET_KEY and ALGORITHM.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the email from the token payload. The email is stored in the "sub" claim.
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # Raise the exception if there is any error during token decoding.
        raise credentials_exception

    # Query the database to retrieve the user with the corresponding email.
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        # If the user is not found, raise unauthorized exception.
        raise credentials_exception

    # Return the authenticated user instance.
    return user
