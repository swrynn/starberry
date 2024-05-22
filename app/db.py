"""
Followed the guide from here: https://docs.litestar.dev/2/usage/databases/sqlalchemy/models_and_repository.html#basic-use
"""

from __future__ import annotations
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
)


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"


session_config = AsyncSessionConfig(
    expire_on_commit=False,
)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=SQLALCHEMY_DATABASE_URL,
    session_config=session_config,
    create_all=True,
)


sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
