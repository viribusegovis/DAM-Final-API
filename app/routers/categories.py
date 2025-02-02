from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Category, RecipeCategory, User
from app.schemas import CategoryResponse, CategoryCreate
from app.security.dependencies import get_current_user

# Initialize API router for category endpoints.
router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    This endpoint returns a list of all category records from the database.

    Args:
        db (Session): The SQLAlchemy database session, provided by dependency injection.

    Returns:
        List[CategoryResponse]: A list of categories available in the system.
    """
    categories = db.query(Category).all()
    return categories


@router.get("/top", response_model=List[CategoryResponse])
def get_top_categories(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve the top categories based on recipe usage.

    This endpoint joins the Category table with RecipeCategory to count how many recipes
    are associated with each category. It groups by all category attributes, orders the results
    by the count in descending order, and returns the top categories up to the specified limit.

    Args:
        limit (int, optional): The maximum number of top categories to return. Defaults to 10.
        db (Session): The SQLAlchemy database session.

    Returns:
        List[CategoryResponse]: A list of the top categories; if none are found, an empty list is returned.
    """
    top_categories = (
        db.query(
            Category.category_id,
            Category.name,
            Category.description,
            Category.image_url
        )
        .join(RecipeCategory)
        .group_by(
            Category.category_id,
            Category.name,
            Category.description,
            Category.image_url
        )
        .order_by(func.count(RecipeCategory.recipe_id).desc())
        .limit(limit)
        .all()
    )

    if not top_categories:
        return []
    return top_categories


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new category.

    This endpoint allows an authenticated user to create a new category record in the database.

    Args:
        category (CategoryCreate): The category data required for creation.
        db (Session): The SQLAlchemy database session, provided via dependency injection.
        current_user (User): The currently authenticated user, provided by the authentication dependency.

    Returns:
        CategoryResponse: The details of the newly created category.
    """
    new_category = Category(
        name=category.name,
        description=category.description,
        image_url=category.image_url
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
