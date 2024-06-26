"""
A module for resolvers in the app.api.graphql.resolvers package.
"""

from app.db.init_db import employers, jobs

# def resolve_employer(id):
#     return None


def resolver_employers() -> list[dict[str, int | str]]:
    return employers


def resolver_jobs() -> list[dict[str, int | str]]:
    return jobs
