"""
A module for job queries in the app.api.graphql.queries package.
"""

from typing import Any, Optional

from graphene import Field, Int, List, ObjectType
from graphql.type.definition import GraphQLResolveInfo
from pydantic import PositiveInt

from app.api.graphql.resolvers.job import resolver_job, resolver_jobs
from app.api.graphql.types.job import Job as JobType
from app.models.job import Job


class JobQuery(ObjectType):  # type: ignore
    jobs = List(JobType)
    job = Field(JobType, id=Int(required=True))

    @staticmethod
    async def resolve_job(
        root: Optional[Any],
        info: Optional[GraphQLResolveInfo],
        _id: PositiveInt,
    ) -> Job:
        return await resolver_job(_id)

    @staticmethod
    async def resolve_jobs(
        root: Optional[Any], info: Optional[GraphQLResolveInfo]
    ) -> list[Job]:
        return await resolver_jobs()
