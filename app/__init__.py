import strawberry

from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from litestar.plugins.structlog import StructlogPlugin
from strawberry.litestar import make_graphql_controller
from strawberry.tools import merge_types

from .users import UsersQuery
from .db import on_startup, sqlalchemy_config
from .custom_context import custom_context_getter


@get("/")
def health() -> dict[str, bool]:
    """
    Just a simple health checker to know if base server is running fine.
    """

    return {"ok": True}


# https://strawberry.rocks/docs/guides/tools#merge_types
ComboQuery = merge_types("ComboQuery", (UsersQuery,))
schema = strawberry.Schema(query=ComboQuery)

GraphQLController = make_graphql_controller(
    schema,
    context_getter=custom_context_getter,
    debug=True,
    path="/graphql",
)


app = Litestar(
    on_startup=[on_startup],
    plugins=[
        StructlogPlugin(),
        SQLAlchemyInitPlugin(config=sqlalchemy_config),
    ],
    route_handlers=[
        health,
        GraphQLController,
    ],
)
