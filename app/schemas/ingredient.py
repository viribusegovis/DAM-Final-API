from typing import Optional
from pydantic import BaseModel


class IngredientBase(BaseModel):
    """
    Base schema for an ingredient with common fields.

    Attributes:
        name (str): The name of the ingredient.
        image_url (Optional[str]): An optional URL pointing to an image of the ingredient.
    """
    name: str
    image_url: Optional[str] = None


class IngredientCreate(IngredientBase):
    """
    Schema for creating a new ingredient.

    Inherits all attributes from IngredientBase.
    """
    pass


class IngredientResponse(IngredientBase):
    """
    Schema for returning ingredient details in API responses.

    Extends IngredientBase by adding:
        ingredient_id (int): The unique identifier for the ingredient.
    """
    ingredient_id: int
