"""
A module for user in the app.api.graphql.queries package.
"""

from typing import Any, Optional

from graphene import Field, Int, List, ObjectType
from graphql.type.definition import GraphQLResolveInfo
from pydantic import PositiveInt

from app.api.graphql.resolvers.user import resolver_user, resolver_users
from app.api.graphql.types.user import UserType
from app.models.user import User


class UserQuery(ObjectType):  # type: ignore
    users = List(UserType)
    user = Field(UserType, id=Int(required=True))

    @staticmethod
    async def resolve_users(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[User]:
        return await resolver_users()

    @staticmethod
    async def resolve_user(
        root: Optional[Any],
        info: Optional[GraphQLResolveInfo],
        _id: PositiveInt,
    ) -> User:
        return await resolver_user(_id)
