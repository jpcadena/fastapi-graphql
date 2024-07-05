"""
A module for employer in the app.api.graphql.types package.
"""

from typing import Optional

from graphene import Int, List, ObjectType, String
from graphql.type.definition import GraphQLResolveInfo
from sqlalchemy.orm import InstrumentedAttribute

from app.models.employer import Employer
from app.models.job import Job


class EmployerType(ObjectType):  # type: ignore
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List("app.api.graphql.types.job.JobType")

    @staticmethod
    def resolve_jobs(
        root: Optional[Employer], info: Optional[GraphQLResolveInfo]
    ) -> list[Job]:
        if root is None:
            return []
        if isinstance(root.jobs, InstrumentedAttribute):
            return root.jobs.all()
        return root.jobs
