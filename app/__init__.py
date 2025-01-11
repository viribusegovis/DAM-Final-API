from fastapi import FastAPI

from app.database import engine
from app.models.base import Base
from app.routers import users, recipes, instructions, ingredients

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(instructions.router)
app.include_router(ingredients.router)
