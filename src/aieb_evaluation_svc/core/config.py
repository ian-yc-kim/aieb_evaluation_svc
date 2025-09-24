from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///:memory:"
    SERVICE_PORT: int = 8000
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    REDIS_BROKER_URL: str = "redis://localhost:6379/0"

settings = Settings()
