"""
A module for employer queries in the app.api.graphql.queries package.
"""

from typing import Any, Optional

from graphene import Field, Int, List, ObjectType
from graphql.type.definition import GraphQLResolveInfo
from pydantic import PositiveInt

from app.api.graphql.resolvers.employer import (
    resolver_employer,
    resolver_employers,
)
from app.api.graphql.types.employer import Employer as EmployerType
from app.models.employer import Employer


class EmployerQuery(ObjectType):  # type: ignore
    employers = List(EmployerType)
    employer = Field(EmployerType, id=Int(required=True))

    @staticmethod
    async def resolve_employer(
        root: Optional[Any],
        info: Optional[GraphQLResolveInfo],
        _id: PositiveInt,
    ) -> Employer:
        return await resolver_employer(_id)

    @staticmethod
    async def resolve_employers(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[Employer]:
        return await resolver_employers()
