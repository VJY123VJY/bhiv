from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "BHIV Intelligence Data Universe Registry"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://bhiv:bhiv_secret@localhost:5432/bhiv_registry"

    REGISTRY_ID: str = "BHIV-IDU-REGISTRY-V1"
    TANTRA_ECOSYSTEM_VERSION: str = "V1"

    # MDU Configuration
    MDU_BASE_URL: str = "http://localhost:8000"
    MDU_API_KEY: str = ""
    MDU_API_TIMEOUT: int = 10
    MDU_ALLOW_TRUST_LEVELS: list[str] = ["TRUSTED", "VERIFIED"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()