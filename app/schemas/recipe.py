from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.recipe_ingredient import RecipeIngredientResponse
from app.schemas.category import CategoryResponse
from app.schemas.ingredient import IngredientResponse


class RecipeBase(BaseModel):
    title: str
    description: Optional[str]
    preparation_time: int
    servings: int
    difficulty: str
    image_url: Optional[str]


class RecipeCreate(RecipeBase):
    # Inherits all fields from RecipeBase and adds:
    author_id: int

    # Contains:
    # - title: str
    # - description: Optional[str]
    # - preparation_time: int
    # - servings: int
    # - difficulty: str
    # - category: str
    # - image_url: Optional[str]
    # - author_id: int


class RecipeResponse(RecipeBase):
    id: int
    created_at: datetime
    categories: List[CategoryResponse]
    ingredients: List[RecipeIngredientResponse]

    # Contains:
    # - title: str
    # - description: Optional[str]
    # - preparation_time: int
    # - servings: int
    # - difficulty: str
    # - category: str
    # - image_url: Optional[str]
    # - id: int
    # - created_at: datetime

    class Config:
        from_attributes = True
