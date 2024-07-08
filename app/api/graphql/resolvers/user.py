"""
A module for user in the app.api.graphql.resolvers package.
"""

from pydantic import PositiveInt
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.exceptions.exceptions import DatabaseException
from app.models.user import User


async def resolver_users() -> list[User]:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        result: Result[tuple[User]] = await session.execute(select(User))
    return list(result.scalars().all())


async def resolver_user(_id: PositiveInt) -> User:
    async_session: AsyncSession = await get_session()
    async with async_session as session:
        job = await session.get(User, _id)
        if not job:
            raise DatabaseException("User not found")
    return User(job)
