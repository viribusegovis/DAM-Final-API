from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)
    image_url = Column(String)
