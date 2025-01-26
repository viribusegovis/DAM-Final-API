from pydantic import BaseModel

from app.schemas.ingredient import IngredientResponse


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: float
    unit: str


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    ingredient: IngredientResponse

    class Config:
        from_attributes = True