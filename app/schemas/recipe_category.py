from pydantic import BaseModel


class RecipeCategoryBase(BaseModel):
    """
    Base model for associating a recipe with a category.

    Attributes:
        recipe_id (int): The identifier of the recipe.
        category_id (int): The identifier of the category.
    """
    recipe_id: int
    category_id: int


class RecipeCategoryCreate(RecipeCategoryBase):
    """
    Model used when creating a new recipe-category association.

    Inherits all fields from RecipeCategoryBase. This model is used for input data when
    linking a recipe to a category.
    """
    pass


class RecipeCategoryResponse(RecipeCategoryBase):
    """
    Model used to return details of a recipe-category association in API responses.

    Inherits all fields from RecipeCategoryBase. This model is used for output data and
    can be further extended with additional response fields if needed.
    """
    pass
