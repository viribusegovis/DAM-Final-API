from fastapi import FastAPI
from app.database import engine
from app.models.base import Base


def create_app():
    """
    Factory function to create and configure a FastAPI application instance.

    This function performs the following tasks:
      - Initializes a new FastAPI application.
      - Creates all database tables from the SQLAlchemy models defined in Base.
      - Imports and includes the routers for authentication, users, recipes, instructions,
        ingredients, and categories.
      - Defines a simple root endpoint that returns a welcome message.

    Returns:
        FastAPI: The configured FastAPI application instance.

    Example:
        app = create_app()
    """
    app = FastAPI()

    # Create database tables based on the models defined in Base.
    Base.metadata.create_all(bind=engine)

    # Import routers from various modules to set up endpoint routes.
    from app.routers import users, recipes, instructions, ingredients, auth, categories

    # Include the imported routers in the application.
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(recipes.router)
    app.include_router(instructions.router)
    app.include_router(ingredients.router)
    app.include_router(categories.router)

    # Define a simple route for the root URL that returns a welcome message.
    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Recipe API"}

    return app
