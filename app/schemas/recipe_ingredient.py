from pydantic import BaseModel
from app.schemas.ingredient import IngredientResponse


class RecipeIngredientBase(BaseModel):
    """
    Base model for RecipeIngredient containing common fields used in both creation and response schemas.

    Attributes:
        ingredient_id (int): The unique identifier of the ingredient.
        amount (float): The quantity of the ingredient needed.
        unit (str): The unit of measurement for the ingredient (e.g., grams, cups).
        ingredient (IngredientResponse): Detailed information about the ingredient, provided as a nested response model.
    """
    ingredient_id: int
    amount: float
    unit: str
    ingredient: IngredientResponse


class RecipeIngredientCreate(RecipeIngredientBase):
    """
    Model for creating a new RecipeIngredient entry.

    Inherits all fields from RecipeIngredientBase. Note that the recipe_id field is intentionally
    omitted in the creation schema, as it is associated later when linking the ingredient to a recipe.
    """
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    """
    Model for returning RecipeIngredient details in API responses.

    Extends RecipeIngredientBase by including the recipe_id, which indicates the recipe this
    ingredient is associated with.

    Attributes:
        recipe_id (int): Identifier of the associated recipe.
    """
    recipe_id: int

    class Config:
        from_attributes = True
