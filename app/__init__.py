from fastapi import FastAPI
from app.database import engine
from app.models.base import Base


def create_app():
    app = FastAPI()

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Import and include routers
    from app.routers import users, recipes, instructions, ingredients, auth, categories

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(recipes.router)
    app.include_router(instructions.router)
    app.include_router(ingredients.router)
    app.include_router(categories.router)

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Recipe API"}

    return app
