"""
A module for combining all queries in the app.api.graphql.queries package.
"""

from graphene import ObjectType

from .employer import EmployerQuery
from .job import JobQuery


class Query(JobQuery, EmployerQuery, ObjectType):  # type: ignore
    pass
