"""
A module for user in the app.api.graphql.types package.
"""

from typing import Optional

from graphene import Int, List, ObjectType, String
from graphql import GraphQLResolveInfo

from app.models.application import Application
from app.models.user import User


class UserType(ObjectType):  # type: ignore
    id = Int()
    username = String()
    email = String()
    role = String()
    applications = List("app.api.graphql.types.application.ApplicationType")

    @staticmethod
    def resolve_applications(
        root: Optional[User], info: Optional[GraphQLResolveInfo]
    ) -> list[Application] | None:
        return None if root is None else root.applications


__all__ = ["UserType"]
