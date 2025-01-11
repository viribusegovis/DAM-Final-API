import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    SERVER: str = os.getenv("DB_SERVER")
    DATABASE: str = os.getenv("DB_NAME")
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DRIVER: str = "{ODBC Driver 18 for SQL Server}"


settings = Settings()
