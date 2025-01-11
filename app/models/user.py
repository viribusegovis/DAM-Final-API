from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.models.base import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
