from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Add backend to path so we can import our models
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.base import Base
from app.models import registry  # ensures all models are loaded
from app.core.config import settings
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata for autogenerate
target_metadata = Base.metadata

# Override sqlalchemy.url from our settings
# Convert the asyncpg URL to a psycopg2-compatible URL for Alembic
db_url = settings.DATABASE_URL
if "postgresql+asyncpg" in db_url:
    parsed = urlparse(db_url)
    scheme = "postgresql+psycopg2"
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))

    # asyncpg variant uses `ssl` (we convert from sslmode->ssl earlier).
    # psycopg2 expects `sslmode`, not `ssl`. Convert back when present.
    if "ssl" in query:
        query["sslmode"] = query.pop("ssl")

    updated = parsed._replace(scheme=scheme, query=urlencode(query, doseq=True))
    db_url_for_alembic = urlunparse(updated)
else:
    db_url_for_alembic = db_url.replace("postgresql+asyncpg", "postgresql+psycopg2")

config.set_main_option("sqlalchemy.url", db_url_for_alembic)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()