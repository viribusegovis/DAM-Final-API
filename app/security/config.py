from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.config import settings

# Configuration from settings for JWT processing.
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Create a cryptographic context for hashing passwords using bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize the OAuth2 password bearer scheme, which expects a token at the "token" URL.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the provided plain text password matches the stored hashed password.

    This function uses the passlib CryptContext configured to use the bcrypt algorithm.
    It compares the plain_password with the hashed_password and returns a boolean result.

    Parameters:
        plain_password (str): The plain text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: str) -> str:
    """
    Generate a new JWT access token for the given user email.

    The token includes:
      - "sub": set to the user's email, used as the subject of the token.
      - "exp": the expiration time, calculated as the current time plus the configured token lifetime.

    The JWT token is then encoded using the SECRET_KEY and ALGORITHM defined in the configuration.

    Parameters:
        email (str): The email of the user who is being authenticated.

    Returns:
        str: The encoded JWT token as a string.
    """
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
