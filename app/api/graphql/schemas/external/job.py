"""
A module for job in the app.api.graphql.schemas.external package.
"""

from typing import Any, Optional

from graphene import Field, Int, ObjectType, String

from app.db.init_db import employers


class Job(ObjectType):  # type: ignore
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field("app.api.graphql.schemas.external.employer.Employer")

    @staticmethod
    def resolve_employer(
        root: Optional[dict[str, Any]], info: Optional[Any]
    ) -> dict[str, int | str]:
        return next(
            (
                employer
                for employer in employers
                if employer["id"] == root["employer_id"]
            ),
            None,
        )
