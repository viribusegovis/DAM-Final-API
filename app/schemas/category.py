from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    """
    Base schema for a category with common fields.

    Attributes:
        name (str): The name of the category.
        description (Optional[str]): A brief description of the category.
        image_url (Optional[str]): An optional URL pointing to an image for the category.
    """
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.

    Inherits all attributes from CategoryBase.
    """
    pass


class CategoryResponse(CategoryBase):
    """
    Schema for returning category details in API responses.

    Extends CategoryBase by adding:
        category_id (int): The unique identifier for the category.
    """
    category_id: int
