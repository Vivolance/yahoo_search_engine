from logging.config import fileConfig
from typing import Any

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from src.utils.construct_connection_string import construct_sqlalchemy_url_from_env_vars
from database_management.tables import main_metadata

config = context.config

# Interpret the local_config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = main_metadata

# other values from the local_config, defined by the needs of env.py,
# can be acquired:
# my_important_option = local_config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url: str = construct_sqlalchemy_url_from_env_vars(use_async_pg=False)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    Hack: We override alembic to let us dynamically
    construct the url used for alembic, with environment variables
    - We had to do this, as alembic.ini doesn't
    support constructing url from environment variables
    """
    alembic_config: dict[str, Any] = config.get_section(config.config_ini_section, {})
    alembic_config["sqlalchemy.url"] = construct_sqlalchemy_url_from_env_vars(
        use_async_pg=False
    )
    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
