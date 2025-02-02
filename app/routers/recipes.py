from operator import or_
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.config import settings
from app.database import get_db
from app.models import RecipeIngredient, Ingredient, Category, User
from app.models.instruction import Instruction
from app.models.recipe import Recipe
from app.models.recipe_category import RecipeCategory
from app.schemas import RecipeIngredientResponse
from app.schemas.instruction import InstructionResponse
from app.schemas.recipe import RecipeResponse, RecipeCreate
from app.security.dependencies import get_current_user, oauth2_scheme

# Initialize the API router for recipe-related endpoints.
router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=List[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    """
    Retrieve all recipes.

    This endpoint fetches all recipe entries from the database.

    Args:
        db (Session): The SQLAlchemy database session provided by dependency injection.

    Returns:
        List[RecipeResponse]: A list of recipes available in the system.
    """
    recipes = db.query(Recipe).all()
    return recipes


@router.get("/author/", response_model=List[RecipeResponse])
def get_recipes_by_author(
        author_id: int,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Retrieve recipes created by a specific author.

    This endpoint extracts the current user's email from the provided token and then fetches
    the recipes that belong to that user (by author_id).

    Args:
        author_id (int): The author's unique identifier.
        token (str): JWT token extracted by the OAuth2PasswordBearer dependency.
        db (Session): The database session.

    Raises:
        HTTPException: If credentials are invalid or user not found.

    Returns:
        List[RecipeResponse]: A list of recipes created by the specified author.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token to retrieve payload.
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    recipes = (
        db.query(Recipe)
        .filter(Recipe.author_id == user.user_id)
        .all()
    )
    # Return an empty list if no recipes are found.
    if not recipes:
        return []
    return recipes


@router.get("/category/{category_id}", response_model=List[RecipeResponse])
def get_recipes_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve recipes filtered by a specific category.

    This endpoint returns recipes that are associated with the given category_id.

    Args:
        category_id (int): Unique identifier for the category.
        db (Session): The database session provided by dependency injection.

    Returns:
        List[RecipeResponse]: A list of recipes matching the specified category.
    """
    recipes = (
        db.query(Recipe)
        .join(RecipeCategory)
        .join(Category)
        .filter(Category.category_id == category_id)
        .all()
    )
    if not recipes:
        return []
    return recipes


@router.get("/ingredient/{ingredient_id}", response_model=List[RecipeResponse])
def get_recipes_by_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """
    Retrieve recipes that use a specific ingredient.

    This endpoint finds recipes which include the specified ingredient_id.

    Args:
        ingredient_id (int): Unique identifier for the ingredient.
        db (Session): The SQLAlchemy database session.

    Returns:
        List[RecipeResponse]: A list of recipes containing the ingredient.
    """
    recipes = (
        db.query(Recipe)
        .join(RecipeIngredient)
        .join(Ingredient)
        .filter(Ingredient.ingredient_id == ingredient_id)
        .all()
    )
    if not recipes:
        return []
    return recipes


@router.get("/search", response_model=List[RecipeResponse])
def search_recipes(query: str, db: Session = Depends(get_db)):
    """
    Search for recipes that match the provided query.

    The search is performed across the recipe title, description, ingredient names,
    and category names. Matching is performed in a case-insensitive manner using SQL ILIKE.

    Args:
        query (str): The search query string.
        db (Session): The database session.

    Returns:
        List[RecipeResponse]: A list of recipes that match the search criteria.
    """
    recipes = (
        db.query(Recipe)
        .join(RecipeIngredient)
        .join(Ingredient)
        .join(RecipeCategory)
        .join(Category)
        .filter(
            or_(
                Recipe.title.ilike(f"%{query}%"),
                or_(
                    Recipe.description.ilike(f"%{query}%"),
                    or_(
                        Ingredient.name.ilike(f"%{query}%"),
                        Category.name.ilike(f"%{query}%")
                    )
                )
            )
        )
        .distinct()  # Ensure unique recipes in case of multiple joins.
        .order_by(Recipe.title)
        .all()
    )
    return recipes or []


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the details of a specific recipe.

    Args:
        recipe_id (int): The unique identifier of the recipe.
        db (Session): The database session provided by dependency injection.

    Raises:
        HTTPException: If the recipe with the given recipe_id is not found.

    Returns:
        RecipeResponse: Detailed information on the requested recipe.
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/{recipe_id}/ingredients", response_model=List[RecipeIngredientResponse])
def get_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of ingredients for a specific recipe.

    Args:
        recipe_id (int): The unique identifier of the recipe.
        db (Session): The database session.

    Raises:
        HTTPException: If no ingredients are found for the given recipe.

    Returns:
        List[RecipeIngredientResponse]: A list of ingredients with their amounts and units.
    """
    ingredients = (
        db.query(RecipeIngredient)
        .join(Ingredient)
        .filter(RecipeIngredient.recipe_id == recipe_id)
        .all()
    )
    if not ingredients:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return ingredients


@router.get("/{recipe_id}/instructions", response_model=List[InstructionResponse])
def get_recipe_instructions(recipe_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of instructions for a specific recipe.

    Args:
        recipe_id (int): The unique identifier of the recipe.
        db (Session): The SQLAlchemy database session.

    Raises:
        HTTPException: If no instructions are found for the given recipe.

    Returns:
        List[InstructionResponse]: A list of instruction steps in order.
    """
    instructions = (
        db.query(Instruction)
        .join(Recipe)
        .filter(recipe_id == Recipe.id)
        .all()
    )
    if not instructions:
        raise HTTPException(status_code=404, detail="Instructions not found")
    return instructions


@router.post("/", response_model=RecipeResponse)
def create_recipe(
        recipe: RecipeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Create a new recipe.

    This endpoint handles the creation of a new recipe, including its categories, ingredients,
    and instructions. It first creates the basic recipe record, then iterates over the provided
    categories, ingredients, and instructions to create associated records.

    Args:
        recipe (RecipeCreate): The recipe details for creation.
        db (Session): The SQLAlchemy database session.
        current_user (User): The user creating the recipe (extracted from the auth token).

    Returns:
        RecipeResponse: The newly created recipe with all associated details.
    """
    # Create the base recipe record.
    new_recipe = Recipe(
        title=recipe.title,
        description=recipe.description,
        preparation_time=recipe.preparation_time,
        servings=recipe.servings,
        difficulty=recipe.difficulty,
        image_url=recipe.image_url,
        author_id=current_user.user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    # Link categories to the recipe.
    for category in recipe.categories:
        recipe_category = RecipeCategory(
            recipe_id=new_recipe.id,
            category_id=category.category_id
        )
        db.add(recipe_category)

    # Add recipe ingredients with amounts and units.
    for ingredient in recipe.ingredients:
        recipe_ingredient = RecipeIngredient(
            recipe_id=new_recipe.id,
            ingredient_id=ingredient.ingredient_id,
            amount=ingredient.amount,
            unit=ingredient.unit
        )
        db.add(recipe_ingredient)

    # Add step-by-step instructions.
    for idx, instruction in enumerate(recipe.instructions, 1):
        new_instruction = Instruction(
            recipe_id=new_recipe.id,
            step_number=idx,
            instruction_text=instruction
        )
        db.add(new_instruction)

    # Finalize all creations and refresh the recipe record.
    db.commit()
    db.refresh(new_recipe)
    return new_recipe
