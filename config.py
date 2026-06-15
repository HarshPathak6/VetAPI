# Config.py
# ds values from .env file

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database connection string loaded from .env
    DATABASE_URL: str

    # Tell Pydantic where to look for environment variables
    model_config = SettingsConfigDict(
        env_file=".env"
    )

# Create a settings object that can be imported throughout the project
settings = Settings()
