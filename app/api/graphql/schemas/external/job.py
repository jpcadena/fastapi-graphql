"""
A module for job in the app.api.graphql.schemas.external package.
"""

from typing import Optional, Union

from graphene import Field, Int, ObjectType, String
from graphql.type.definition import GraphQLResolveInfo

from app.db.init_db import employers
from app.models.job import Job as JobModel


class Job(ObjectType):  # type: ignore
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field("app.api.graphql.schemas.external.employer.Employer")

    @staticmethod
    def resolve_employer(
        root: Optional[JobModel], info: Optional[GraphQLResolveInfo]
    ) -> Optional[dict[str, Union[int, str]]]:
        if root is None:
            return None
        return next(
            (
                employer
                for employer in employers
                if employer["id"] == root.employer_id
            ),
            None,
        )
