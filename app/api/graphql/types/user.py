"""
A module for user in the app.api.graphql.types package.
"""

from graphene import Int, ObjectType, String


class User(ObjectType):  # type: ignore
    id = Int()
    username = String()
    email = String()
    role = String()


__all__ = ["User"]
