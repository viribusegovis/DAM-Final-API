from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecipeIngredient, User
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientResponse, IngredientCreate
from app.security.dependencies import get_current_user

# Initialize API router for ingredient endpoints.
router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=List[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    """
    Retrieve all ingredients from the database.

    Args:
        db (Session): SQLAlchemy session provided by dependency injection.

    Returns:
        List[IngredientResponse]: A list of all ingredients.
    """
    ingredients = db.query(Ingredient).all()
    return ingredients


@router.get("/top/{limit}", response_model=List[IngredientResponse])
def get_top_ingredients(limit: int, db: Session = Depends(get_db)):
    """
    Retrieve the top ingredients based on their frequency of appearance in recipes.

    This endpoint joins the Ingredient table with RecipeIngredient to perform a count of how many
    recipes include each ingredient, groups by the ingredient attributes, orders in descending
    order of usage count, and applies a limit to the results.

    Args:
        limit (int): The maximum number of top ingredients to return.
        db (Session): SQLAlchemy session for database interaction.

    Returns:
        List[IngredientResponse]: A list of top ingredients; returns an empty list if none are found.
    """
    top_ingredients = (
        db.query(Ingredient.ingredient_id, Ingredient.name, Ingredient.image_url)
        .join(RecipeIngredient)
        .group_by(Ingredient.ingredient_id, Ingredient.name, Ingredient.image_url)
        .order_by(func.count(RecipeIngredient.recipe_id).desc())
        .limit(limit)
        .all()
    )

    if not top_ingredients:
        return []
    return top_ingredients


@router.get("/search", response_model=List[IngredientResponse])
def search_recipes(query: str, db: Session = Depends(get_db)):
    """
    Search for ingredients that match the provided query.

    This endpoint performs a case-insensitive search on the ingredient name using SQL ILIKE.
    It returns a distinct ordered list of ingredients that match the search term.

    Args:
        query (str): The search string to match ingredient names.
        db (Session): The SQLAlchemy database session provided by dependency injection.

    Returns:
        List[IngredientResponse]: A list of ingredients matching the given query, or an empty list if none match.
    """
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.name.ilike(f"%{query}%"))
        .distinct()
        .order_by(Ingredient.name)
        .all()
    )
    return ingredients or []


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific ingredient by its unique identifier.

    Args:
        ingredient_id (int): The unique identifier of the ingredient to retrieve.
        db (Session): SQLAlchemy session provided through dependency injection.

    Raises:
        HTTPException: If the ingredient with the given id is not found.

    Returns:
        IngredientResponse: The details of the requested ingredient.
    """
    ingredient = db.query(Ingredient).filter(
        Ingredient.ingredient_id == ingredient_id
    ).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.post("/", response_model=IngredientResponse)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new ingredient in the database.

    This endpoint creates a new ingredient record with the provided data.
    It requires an authenticated user to perform the action.

    Args:
        ingredient (IngredientCreate): The schema containing the data for the new ingredient.
        db (Session): The SQLAlchemy database session provided via dependency injection.
        current_user (User): The currently authenticated user, provided by the auth dependency.

    Returns:
        IngredientResponse: The newly created ingredient's details.
    """
    new_ingredient = Ingredient(
        name=ingredient.name
        # image_url can be set here if available, e.g., image_url=ingredient.image_url
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient
