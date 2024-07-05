"""
A module for job in the app.api.graphql.types package.
"""

from typing import Optional

from graphene import Field, Int, List, ObjectType, String
from graphql.type.definition import GraphQLResolveInfo

from app.models.application import Application
from app.models.employer import Employer
from app.models.job import Job


class JobType(ObjectType):  # type: ignore
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field("app.api.graphql.types.employer.EmployerType")
    applications = List("app.api.graphql.types.application.ApplicationType")

    @staticmethod
    def resolve_employer(
        root: Optional[Job], info: Optional[GraphQLResolveInfo]
    ) -> Employer | None:
        return None if root is None else root.employer

    @staticmethod
    def resolve_applications(
        root: Optional[Job], info: Optional[GraphQLResolveInfo]
    ) -> list[Application] | None:
        return None if root is None else root.applications
