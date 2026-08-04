from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

ROOT_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    APP_NAME: str = "BHIV Intelligence Data Universe Registry"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://bhiv_user:XCDSC9O2DEqqcYr5eJdVQW5BnhN7pzJ0@dpg-d9o7s98ae00c73atq3j0-a.oregon-postgres.render.com/bhiv?sslmode=require"

    REGISTRY_ID: str = "BHIV-IDU-REGISTRY-V1"
    TANTRA_ECOSYSTEM_VERSION: str = "V1"

    # MDU Configuration
    MDU_BASE_URL: str = "http://localhost:8000"
    MDU_API_KEY: str = ""
    MDU_API_TIMEOUT: int = 10
    MDU_ALLOW_TRUST_LEVELS: list[str] = ["TRUSTED", "VERIFIED"]

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

        # asyncpg does not accept sslmode as a direct connect argument.
        # Convert sslmode to ssl when using asyncpg and ensure SSL is required
        # for non-local PostgreSQL hosts.
        if "sslmode" in query:
            query["ssl"] = query.pop("sslmode")

        if "ssl" not in query:
            query["ssl"] = "require"

        scheme = parsed.scheme
        if scheme == "postgres":
            scheme = "postgresql+asyncpg"
        elif scheme == "postgresql" and "+asyncpg" not in value:
            scheme = "postgresql+asyncpg"

        updated = parsed._replace(scheme=scheme, query=urlencode(query, doseq=True))
        return urlunparse(updated)

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()