"""
This module sets up the database connection using SQLAlchemy and provides a database session dependency.

The connection is created using the connection string composed from configuration settings.
A sessionmaker is then configured for creating new database sessions which can be used in API endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Build the database connection string using the configuration settings.
# The connection string follows the format for a Microsoft SQL Server connection via pymssql:
# "mssql+pymssql://username:password@server/database"
connection_string = (
    f"mssql+pymssql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
    f"@{settings.SERVER}/{settings.DATABASE}"
)

# Create the SQLAlchemy engine using the constructed connection string.
# This engine will manage the connection pool to the database.
engine = create_engine(connection_string)

# Create a configured "SessionLocal" class.
# This sessionmaker is bound to our engine and is configured not to autocommit or autoflush.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency generator that creates a new SQLAlchemy database session.

    This function creates a new session using SessionLocal, yields it to the caller (e.g., API endpoints),
    and ensures that the session is properly closed after use, even if an exception occurs.

    Yields:
        db (Session): A SQLAlchemy session instance for performing database operations.

    Usage Example:
        In FastAPI, you can use this dependency in a route like so:

        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
