import uvicorn
from fastapi import FastAPI

from app.database import engine
from app.models.base import Base
from app.routers import users, recipes, auth

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Recipe API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)