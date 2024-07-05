"""
A module for combining all queries in the app.api.graphql.queries package.
"""

from graphene import ObjectType

from .application import ApplicationQuery
from .employer import EmployerQuery
from .job import JobQuery
from .user import UserQuery


class Query(
    JobQuery,
    EmployerQuery,
    UserQuery,
    ApplicationQuery,
    ObjectType,  # type: ignore
):
    pass
