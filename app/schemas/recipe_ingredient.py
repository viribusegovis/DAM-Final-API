from pydantic import BaseModel


class RecipeIngredientBase(BaseModel):
    recipe_id: int
    ingredient_id: int
    amount: float
    unit: str


class RecipeIngredientCreate(RecipeIngredientBase):
    pass


class RecipeIngredientResponse(RecipeIngredientBase):
    pass
