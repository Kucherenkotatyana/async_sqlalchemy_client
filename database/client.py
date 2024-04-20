"""
Here we create an Engine associated with a particular database URL.
It will be used later in the process to create a Session that will
execute transactions.
"""
from sqlalchemy.ext.asyncio import create_async_engine

import config

# Configuring database connection URL using provided environment variables.
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
    f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}"
    f"/{config.POSTGRES_DB}"
)

# Using `create_async_engine` method since the connection
# object would be used in async functions, so it must be
# async too.
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)
