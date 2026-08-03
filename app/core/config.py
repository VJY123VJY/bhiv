from pydantic_settings import BaseSettings
<<<<<<< HEAD
from pydantic import field_validator
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
=======
>>>>>>> db763b141a4bb42b0aca956a84f5f73a82c9f518

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

<<<<<<< HEAD
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if not isinstance(value, str):
            return value

        try:
            parsed = urlparse(value)
        except Exception:
            return value

        is_postgres = parsed.scheme in {"postgres", "postgresql", "postgresql+asyncpg"}
        host = parsed.hostname
        local_hosts = {"localhost", "127.0.0.1", "::1"}

        if not is_postgres or host in local_hosts or host is None:
            return value

        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        if "sslmode" not in query:
            query["sslmode"] = "require"

        scheme = parsed.scheme
        if scheme == "postgres":
            scheme = "postgresql+asyncpg"
        elif scheme == "postgresql" and "+asyncpg" not in value:
            scheme = "postgresql+asyncpg"

        updated = parsed._replace(scheme=scheme, query=urlencode(query, doseq=True))
        return urlunparse(updated)

=======
>>>>>>> db763b141a4bb42b0aca956a84f5f73a82c9f518
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()