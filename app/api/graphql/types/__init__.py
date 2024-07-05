"""
Package app.api.graphql.types initialization.
"""

from graphene import ObjectType

from .application import ApplicationType
from .employer import EmployerType
from .job import JobType
from .user import UserType

# Export a list of models in the order you want them called.
__all__: list[ObjectType] = [
    ApplicationType,
    EmployerType,
    JobType,
    UserType,
]
