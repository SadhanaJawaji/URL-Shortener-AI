from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str
    admin_api_key: str
    cors_origins: str = ""
    slug_length: int = 7
    
    class Config:
        env_file = ".env"

settings = Settings()
