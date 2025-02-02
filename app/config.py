import os
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Settings class for application configuration.

    This class loads configuration settings from environment variables using Pydantic's BaseSettings.
    The variables include database connection parameters and JWT authentication settings.

    Attributes:
        SERVER (str): The database server address, read from the environment variable "DB_SERVER".
        DATABASE (str): The name of the database, read from the environment variable "DB_NAME".
        DB_USERNAME (str): The database username, read from the environment variable "DB_USERNAME".
        DB_PASSWORD (str): The database password, read from the environment variable "DB_PASSWORD".
        JWT_SECRET (str): The secret key for JWT token encoding, read from the environment variable "JWT_SECRET".
        JWT_ALGORITHM (str): The algorithm for JWT token encoding, read from the environment variable "JWT_ALGORITHM".
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens (in minutes).

    Example:
        You can instantiate the settings and access configuration values as follows:

            settings = Settings()
            print(settings.SERVER)
    """
    SERVER: str = os.getenv("DB_SERVER")
    DATABASE: str = os.getenv("DB_NAME")
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Creating a global settings instance which will be used throughout the app.
settings = Settings()
