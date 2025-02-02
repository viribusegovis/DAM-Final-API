import uvicorn
from app import create_app

# Create an instance of the FastAPI application using the factory function.
app = create_app()

if __name__ == "__main__":
    # Run the application using Uvicorn on all available IP addresses (0.0.0.0)
    # at port 8080.
    uvicorn.run(app, host="0.0.0.0", port=8080)
