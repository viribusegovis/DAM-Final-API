from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.recipe import Recipe
    from app.models.ingredient import Ingredient

class Instruction(Base):
    __tablename__ = "instructions"
    instruction_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    step_number = Column(Integer, nullable=False)
    instruction_text = Column(String, nullable=False)
    recipe: Mapped[List["Recipe"]] = relationship(back_populates="instructions")

