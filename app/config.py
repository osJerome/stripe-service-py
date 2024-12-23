from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()