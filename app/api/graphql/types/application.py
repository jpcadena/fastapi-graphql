"""
A module for application in the app.api.graphql.types package.
"""

from typing import Optional

from graphene import Field, Int, ObjectType
from graphql import GraphQLResolveInfo

from app.models.application import Application
from app.models.job import Job
from app.models.user import User


class ApplicationType(ObjectType):  # type: ignore
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field("app.api.graphql.types.user.UserType")
    job = Field("app.api.graphql.types.job.JobType")

    @staticmethod
    def resolve_user(
        root: Optional[Application], info: Optional[GraphQLResolveInfo]
    ) -> User | None:
        return None if root is None else root.user

    @staticmethod
    def resolve_job(
        root: Optional[Application], info: Optional[GraphQLResolveInfo]
    ) -> Job | None:
        return None if root is None else root.job


__all__ = ["ApplicationType"]
