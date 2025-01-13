from sqlalchemy import Column, Integer, String, ForeignKey, Numeric

from app.models.base import Base


class RecipeCategory(Base):
    __tablename__ = "recipe_categories"
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.category_id", ondelete="CASCADE"), primary_key=True)
