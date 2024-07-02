"""
A module for job in the app.api.graphql.mutations package.
"""

from typing import Any, Optional

from graphene import Field, Int, Mutation, String
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.graphql.schemas.external.job import Job as JobObject
from app.db.session import get_session
from app.exceptions.exceptions import DatabaseException
from app.models.job import Job


class AddJob(Mutation):  # type: ignore
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    async def mutate(
        root: Optional[Any],
        info: Optional[Any],
        title: str,
        description: str,
        employer_id: PositiveInt,
    ) -> "AddJob":
        job = Job(title=title, description=description, employer_id=employer_id)
        async_session: AsyncSession = await get_session()
        async_session.add(job)
        await async_session.commit()
        return AddJob(job=job)


class UpdateJob(Mutation):  # type: ignore
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    async def mutate(
        root: Optional[Any],
        info: Optional[Any],
        _id: PositiveInt,
        title: Optional[str] = None,
        description: Optional[str] = None,
        employer_id: Optional[PositiveInt] = None,
    ) -> "UpdateJob":
        async_session: AsyncSession = await get_session()
        job = await async_session.get(Job, _id)
        print(type(job))
        if not job:
            raise DatabaseException("Job not found")
        if title is not None:
            job.title = title
            print(type(job.title))
        if description is not None:
            job.description = description
            print(type(job.description))
        if employer_id is not None:
            job.employer_id = employer_id
            print(type(job.employer_id))
        await async_session.commit()
        return UpdateJob(job=job)
