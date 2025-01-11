from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    description: Optional[str]
    preparation_time: int
    servings: int
    difficulty: str
    category: str
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
    # Inherits all fields from RecipeBase and adds:
    id: int
    created_at: datetime

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
