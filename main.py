from fastapi import FastAPI

from app.database import engine
from app.models.base import Base
from app.routers import users, recipes

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(recipes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}
