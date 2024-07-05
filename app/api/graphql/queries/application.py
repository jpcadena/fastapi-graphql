"""
A module for application in the app.api.graphql.queries package.
"""

from typing import Any, Optional

from graphene import List, ObjectType
from graphql.type.definition import GraphQLResolveInfo

from app.api.graphql.resolvers.application import resolver_applications
from app.api.graphql.types.application import ApplicationType
from app.models.application import Application


class ApplicationQuery(ObjectType):  # type: ignore
    applications = List(ApplicationType)

    @staticmethod
    async def resolve_applications(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[Application]:
        return await resolver_applications()
