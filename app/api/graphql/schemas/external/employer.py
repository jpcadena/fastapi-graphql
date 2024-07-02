"""
A module for employer in the app.api.graphql.schemas.external package.
"""

from typing import Optional

from graphene import Int, List, ObjectType, String
from graphql.type.definition import GraphQLResolveInfo

from app.api.graphql.resolvers.resolvers import resolver_jobs
from app.models.employer import Employer as EmployerModel


class Employer(ObjectType):  # type: ignore
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List("app.api.graphql.schemas.external.job.Job")

    @staticmethod
    def resolve_jobs(
        root: Optional[EmployerModel], info: Optional[GraphQLResolveInfo]
    ) -> list[dict[str, int | str]]:
        if root is None:
            return []
        jobs: list[dict[str, int | str]] = resolver_jobs()
        return [job for job in jobs if job["employer_id"] == root.id]
