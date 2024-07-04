"""
A module for employer resolvers in the app.api.graphql.resolvers package.
"""

from pydantic import PositiveInt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.exceptions.exceptions import DatabaseException
from app.models.employer import Employer


async def resolver_employers() -> list[Employer]:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        result: Result[tuple[Employer]] = await session.execute(
            select(Employer)
        )
    return list(result.scalars().all())


async def resolver_employer(_id: PositiveInt) -> Employer:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        employer = await session.get(Employer, _id)
        if not employer:
            raise DatabaseException("Employer not found")
    return Employer(employer)
