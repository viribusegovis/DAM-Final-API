from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Category, RecipeCategory
from app.schemas import CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.get("/top", response_model=List[CategoryResponse])
def get_top_categories(limit: int = 10, db: Session = Depends(get_db)):
    top_categories = (
        db.query(Category.category_id, Category.name, Category.description, Category.image_url)
        .join(RecipeCategory)
        .group_by(Category.category_id, Category.name, Category.description, Category.image_url)
        .order_by(func.count(RecipeCategory.recipe_id).desc())
        .limit(limit)
        .all()
    )

    if not top_categories:
        return []
    return top_categories

