"""
A module for job in the app.api.graphql.types package.
"""

from typing import Optional

from graphene import Field, Int, ObjectType, String
from graphql.type.definition import GraphQLResolveInfo

from app.models.employer import Employer
from app.models.job import Job


class Job(ObjectType):  # type: ignore
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field("app.api.graphql.types.employer.Employer")

    @staticmethod
    def resolve_employer(
        root: Optional[Job], info: Optional[GraphQLResolveInfo]
    ) -> Employer | None:
        return None if root is None else root.employer


__all__ = ["Job"]
