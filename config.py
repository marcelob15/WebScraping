from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DEFAULT_ADMIN_PASSWORD: str
    # Carrega as variáveis a partir de um arquivo .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()