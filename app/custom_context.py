"""
Followed the guide from here: https://strawberry.rocks/docs/integrations/litestar#context_getter
"""

from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.litestar import BaseContext


class CustomContext(BaseContext):
    session: AsyncSession


async def custom_context_getter(
    request: Request, db_session: AsyncSession
) -> CustomContext:
    """
    According to debugger, something fishy going on here!
    """

    return CustomContext(session=db_session)
