"""
A module for employer in the app.api.graphql.schemas.external package.
"""

from typing import Any, Optional

from graphene import Int, List, ObjectType, String

from app.api.graphql.resolvers.resolvers import resolver_jobs


class Employer(ObjectType):  # type: ignore
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List("app.api.graphql.schemas.external.job.Job")

    @staticmethod
    def resolve_jobs(
        root: Optional[dict[str, Any]], info: Optional[Any]
    ) -> list[dict[str, int | str]]:
        jobs: list[dict[str, int | str]] = resolver_jobs()
        return [job for job in jobs if job["employer_id"] == root["id"]]
