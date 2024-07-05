"""
A module for application in the app.api.graphql.resolvers package.
"""

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.application import Application


async def resolver_applications() -> list[Application]:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        result: Result[tuple[Application]] = await session.execute(
            select(Application)
        )
    return list(result.scalars().all())
