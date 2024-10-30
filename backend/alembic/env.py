import asyncio

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

from src.app_config.config_db import db_settings
from src.database.database_metadata import Base

from src.database.all_models import *

config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB", "postgresql+asyncpg")
config.set_section_option(section, "DB_HOST", db_settings.HOST)
config.set_section_option(section, "DB_PORT", db_settings.PORT)
config.set_section_option(section, "DB_NAME", db_settings.NAME)
config.set_section_option(section, "DB_USER", db_settings.USER)
config.set_section_option(section, "DB_PASS", db_settings.PASS)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()