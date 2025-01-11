# Database connection setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database connection setup
connection_string = (
    f"mssql+pymssql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
    f"@{settings.SERVER}/{settings.DATABASE}"
)
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
