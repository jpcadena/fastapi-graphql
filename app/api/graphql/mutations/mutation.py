"""
A module for mutation in the app.api.graphql.mutations package.
"""

from graphene import ObjectType

from app.api.graphql.mutations.employer import (
    AddEmployer,
    DeleteEmployer,
    UpdateEmployer,
)
from app.api.graphql.mutations.job import AddJob, DeleteJob, UpdateJob


class Mutation(ObjectType):  # type: ignore
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()

    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
