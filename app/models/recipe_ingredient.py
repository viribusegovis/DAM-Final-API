from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.ingredient_id", ondelete="CASCADE"), primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="recipes")
