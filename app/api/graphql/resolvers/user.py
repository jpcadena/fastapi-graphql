"""
A module for user in the app.api.graphql.resolvers package.
"""

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User


async def resolver_users() -> list[User]:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        result: Result[tuple[User]] = await session.execute(select(User))
    return list(result.scalars().all())
