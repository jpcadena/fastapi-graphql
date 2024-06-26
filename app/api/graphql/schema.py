"""
A module for schema in the app.api.graphql package.
"""

from typing import Any, Optional

import graphene

from .resolvers.resolvers import resolver_employers, resolver_jobs
from .schemas.external.employer import Employer
from .schemas.external.job import Job


class Query(graphene.ObjectType):  # type: ignore
    jobs = graphene.List(Job)
    employers = graphene.List(Employer)
    # employer = graphene.Field(Employer, id=graphene.Int(required=True))

    @staticmethod
    def resolve_jobs(
        root: Optional[Any], info: Optional[Any]
    ) -> list[dict[str, int | str]]:
        return resolver_jobs()

    @staticmethod
    def resolve_employers(
        root: Optional[Any], info: Optional[Any]
    ) -> list[dict[str, int | str]]:
        return resolver_employers()


schema: graphene.Schema = graphene.Schema(query=Query, types=[Employer, Job])
