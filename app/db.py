"""
Followed the guide from here: https://docs.litestar.dev/2/usage/databases/sqlalchemy/models_and_repository.html#basic-use
"""

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
)


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db"


session_config = AsyncSessionConfig(expire_on_commit=False)


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=SQLALCHEMY_DATABASE_URL,
    session_config=session_config,
)


sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(BigIntAuditBase.metadata.create_all)
