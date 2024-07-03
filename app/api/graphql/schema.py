"""
A module for schema in the app.api.graphql package.
"""

from typing import Any, Optional

from graphene import List, ObjectType, Schema
from graphql.type.definition import GraphQLResolveInfo

from .mutations.mutation import Mutation
from .resolvers.resolvers import resolver_employers, resolver_jobs
from .schemas.external.employer import Employer
from .schemas.external.job import Job


class Query(ObjectType):  # type: ignore
    jobs = List(Job)
    employers = List(Employer)

    # employer = Field(Employer, id=Int(required=True))

    @staticmethod
    def resolve_jobs(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[dict[str, int | str]]:
        return resolver_jobs()

    @staticmethod
    def resolve_employers(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[dict[str, int | str]]:
        return resolver_employers()


schema: Schema = Schema(query=Query, mutation=Mutation, types=[Employer, Job])
