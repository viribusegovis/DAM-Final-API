from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import RecipeIngredient
from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientResponse

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=List[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    ingredients = db.query(Ingredient).all()
    return ingredients


@router.get("/top", response_model=List[IngredientResponse])
def get_top_ingredients(limit: int = 10, db: Session = Depends(get_db)):
    top_ingredients = (
        db.query(Ingredient.ingredient_id, Ingredient.name)
        .join(RecipeIngredient)
        .group_by(Ingredient.ingredient_id, Ingredient.name)
        .order_by(func.count(RecipeIngredient.recipe_id).desc())
        .limit(limit)
        .all()
    )

    if not top_ingredients:
        return []
    return top_ingredients


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(
        Ingredient.ingredient_id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient
