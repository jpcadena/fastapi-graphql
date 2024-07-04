"""
A module for job resolvers in the app.api.graphql.resolvers package.
"""

from pydantic import PositiveInt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.exceptions.exceptions import DatabaseException
from app.models.job import Job


async def resolver_jobs() -> list[Job]:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        result: Result[tuple[Job]] = await session.execute(select(Job))
    return list(result.scalars().all())


async def resolver_job(_id: PositiveInt) -> Job:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        job = await session.get(Job, _id)
        if not job:
            raise DatabaseException("Job not found")
    return Job(job)
