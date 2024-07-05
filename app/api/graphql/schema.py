"""
A module for schema in the app.api.graphql package.
"""

from graphene import Schema

from app.api.graphql.mutations.mutation import Mutation
from app.api.graphql.queries.query import Query
from app.api.graphql.types import __all__ as types

schema: Schema = Schema(
    query=Query,
    mutation=Mutation,
    types=types,
)
