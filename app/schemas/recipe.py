from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.instruction import Instruction  # Imported for potential reference (not directly used here)
from app.schemas import InstructionCreate           # Imported for potential reference (not used in this schema)
from app.schemas.recipe_ingredient import RecipeIngredientResponse, RecipeIngredientCreate
from app.schemas.category import CategoryResponse


class RecipeBase(BaseModel):
    """
    Base schema for recipe objects containing the fundamental fields for a recipe.

    Attributes:
        title (str): The title of the recipe.
        description (Optional[str]): A brief description of the recipe.
        preparation_time (int): Time in minutes required to prepare the recipe.
        servings (int): Number of servings the recipe yields.
        difficulty (str): Recipe difficulty level (e.g., "Easy", "Medium", "Hard").
        image_url (Optional[str]): URL of the recipe image.
    """
    title: str
    description: Optional[str]
    preparation_time: int
    servings: int
    difficulty: str
    image_url: Optional[str]


class RecipeCreate(RecipeBase):
    """
    Schema used when creating a new recipe.

    Inherits from RecipeBase and extends it with additional fields required during recipe creation.

    Attributes:
        author_id (int): The ID of the user creating the recipe.
        categories (List[CategoryResponse]): A list of categories assigned to the recipe.
        ingredients (List[RecipeIngredientCreate]): A list of ingredients required for the recipe,
            using the creation schema for recipe ingredients.
        instructions (List[str]): A list of instruction steps as strings.
    """
    author_id: int
    categories: List[CategoryResponse]
    ingredients: List[RecipeIngredientCreate]
    instructions: List[str]


class RecipeResponse(RecipeBase):
    """
    Schema for returning complete recipe details in API responses.

    This schema extends RecipeBase with system-generated fields and detailed
    associations for categories and ingredients.

    Attributes:
        id (int): The unique identifier of the recipe.
        created_at (datetime): The timestamp when the recipe was created.
        categories (List[CategoryResponse]): Detailed list of categories associated with the recipe.
        ingredients (List[RecipeIngredientResponse]): Detailed list of recipe ingredients.
    """
    id: int
    created_at: datetime
    categories: List[CategoryResponse]
    ingredients: List[RecipeIngredientResponse]

    class Config:
        from_attributes = True
