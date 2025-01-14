from operator import or_
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecipeIngredient, Ingredient, Category
from app.models.recipe import Recipe
from app.models.recipe_category import RecipeCategory
from app.schemas import RecipeIngredientResponse
from app.schemas.recipe import RecipeResponse

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=List[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes


@router.get("/category/{category_id}", response_model=List[RecipeResponse])
def get_recipes_by_category(category_id: int, db: Session = Depends(get_db)):
    recipes = db.query(Recipe).filter(Recipe.category_id == category_id).all()
    if not recipes:
        return []
    return recipes


@router.get("/ingredient/{ingredient_id}", response_model=List[RecipeResponse])
def get_recipes_by_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    recipes = (
        db.query(Recipe)
        .join(RecipeIngredient)
        .filter(RecipeIngredient.ingredient_id == ingredient_id)
        .all()
    )
    if not recipes:
        return []
    return recipes


@router.get("/search", response_model=List[RecipeResponse])
def search_recipes(query: str, db: Session = Depends(get_db)):
    recipes = (
        db.query(Recipe)
        .join(RecipeIngredient)
        .join(Ingredient)
        .join(RecipeCategory)
        .join(Category)
        .filter(
            or_(
                Recipe.title.ilike(f"%{query}%"),
                or_(Recipe.description.ilike(f"%{query}%"),
                    or_(Ingredient.name.ilike(f"%{query}%"),
                        Category.name.ilike(f"%{query}%"))

                    )
            )
        )
        .distinct()
        .order_by(Recipe.title)
        .all()
    )
    return recipes or []


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/{recipe_id}/ingredients", response_model=List[RecipeIngredientResponse])
def get_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    recipe_ingredients = (
        db.query(RecipeIngredient)
        .filter(RecipeIngredient.recipe_id == recipe_id)
        .all()
    )
    if not recipe_ingredients:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_ingredients
