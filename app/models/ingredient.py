from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, Session

from app.models.recipe_ingredient import RecipeIngredient
from app.models.base import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    recipes = relationship('Recipe',
                           secondary=RecipeIngredient.__table__,
                           back_populates='ingredients')
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")