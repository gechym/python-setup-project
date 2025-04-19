from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from _logging import setup_logging

# Load environment variables from .env file


load_dotenv()


class Settings(BaseSettings):
    # Example settings
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str

    LLM_PROVIDER: str
    BASE_URL: str
    OPENAI_API_KEY: str
    PROVIDER_API_KEY: str
    USE_TRACE: bool

    class Config:
        env_file = ".env"  # Specify the .env file to load
        env_file_encoding = "utf-8"


# Create a global settings instance
settings = Settings()


def setup() -> None:
    setup_logging()
    from mutil_agents import setup as mutil_agents_setup

    mutil_agents_setup(
        mongodb_config={
            "host": settings.MONGODB_HOST,
            "port": settings.MONGODB_PORT,
            "username": settings.MONGODB_USERNAME,
            "password": settings.MONGODB_PASSWORD,
        },
        external_config={
            "llm_provider": settings.LLM_PROVIDER,
            "base_url": settings.BASE_URL,
            "openai_api_key": settings.OPENAI_API_KEY,
            "provider_api_key": settings.PROVIDER_API_KEY,
        },
    )
