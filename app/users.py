import strawberry

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from litestar.contrib.sqlalchemy.base import BigIntAuditBase
from pydantic import EmailStr, BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from .custom_context import CustomContext

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(BigIntAuditBase):
    """
    Ref: https://docs.litestar.dev/2/usage/databases/sqlalchemy/models_and_repository.html#basic-use
    """

    email: Mapped[EmailStr] = mapped_column(nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(default=None, nullable=True)


class UserType(BaseModel):
    """
    Ref: https://strawberry.rocks/docs/integrations/pydantic#pydantic-support
    """

    id: int
    email: EmailStr
    full_name: Optional[str] = Field(default=None)
    created_at: datetime
    updated_at: datetime


@strawberry.type
class UserDefinition:
    """
    Ref: https://github.com/strawberry-graphql/examples/blob/main/fastapi-sqlalchemy/api/definitions/movie.py
    """

    id: int
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime

    instance: strawberry.Private[User]

    @classmethod
    def from_instance(cls, instance: User):
        return cls(
            instance=instance,
            **instance.to_dict(),
        )


async def list_users(info: strawberry.Info[CustomContext, None]) -> List[User]:
    """
    Ref: https://strawberry.rocks/docs/integrations/litestar#context_getter
    """

    session: AsyncSession = info.context.session

    query = select(User)
    return list((await session.execute(query)).scalars())


@strawberry.type
class UsersQuery:
    """
    Ref: https://strawberry.rocks/docs#step-4-define-a-resolver
    """

    list_users: List[UserDefinition] = strawberry.field(resolver=list_users)
