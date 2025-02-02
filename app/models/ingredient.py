from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Session

from app.models.recipe_ingredient import RecipeIngredient
from app.models.base import Base
from typing import List
from sqlalchemy.orm import Mapped


class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    image_url = Column(String)
    recipes: Mapped[List["RecipeIngredient"]] = relationship(back_populates="ingredient")
