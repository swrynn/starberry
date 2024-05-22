from __future__ import annotations
from typing import Dict
import strawberry

from litestar import Litestar, get
from litestar.plugins.structlog import StructlogPlugin
from strawberry.litestar import make_graphql_controller
from strawberry.tools import merge_types

from .users import User, UserDefinition, UsersQuery
from .db import sqlalchemy_plugin
from .custom_context import CustomContext, custom_context_getter


@get("/")
def health() -> Dict[str, bool]:
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
    debug=True,
    signature_types=[UserDefinition, User, strawberry.Info, CustomContext],
    plugins=[
        StructlogPlugin(),
        sqlalchemy_plugin,
    ],
    route_handlers=[
        health,
        GraphQLController,
    ],
)
