from pydantic import BaseModel


class RecipeCategoryBase(BaseModel):
    recipe_id: int
    category_id: int


class RecipeCategoryCreate(RecipeCategoryBase):
    pass


class RecipeCategoryResponse(RecipeCategoryBase):
    pass
