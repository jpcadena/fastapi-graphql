"""
A module for user in the app.api.graphql.queries package.
"""

from typing import Any, Optional

from graphene import List, ObjectType
from graphql.type.definition import GraphQLResolveInfo

from app.api.graphql.resolvers.user import resolver_users
from app.api.graphql.types.user import UserType
from app.models.user import User


class UserQuery(ObjectType):  # type: ignore
    users = List(UserType)

    @staticmethod
    async def resolve_users(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[User]:
        return await resolver_users()
