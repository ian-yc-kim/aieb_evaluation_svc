from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///:memory:"
    SERVICE_PORT: int = 8000
    OPENAI_API_KEY: str
    OPENAI_MODEL: str

settings = Settings()
