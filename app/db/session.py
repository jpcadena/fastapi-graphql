"""
Database session script
"""

import logging
from typing import Any, AsyncGenerator, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.config.config import sql_database_setting
from app.core.decorators import benchmark, with_logging

logger: logging.Logger = logging.getLogger(__name__)
url: str = sql_database_setting.SQLALCHEMY_DATABASE_URI.__str__()
async_engine: AsyncEngine = create_async_engine(
    url, pool_pre_ping=True, future=True, echo=True
)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """
    Get an asynchronous session to the database as a generator
    :return session: Async session for database connection
    :rtype session: AsyncSession
    """
    async_session: AsyncSession = AsyncSession(
        bind=async_engine, expire_on_commit=False
    )
    try:
        yield async_session
        await async_session.commit()
    except SQLAlchemyError as exc:
        logger.error(exc)
        await async_session.rollback()
        raise exc


@with_logging
@benchmark
async def get_session() -> AsyncSession:
    """
    Get an asynchronous session to the database
    :return session: Async session for database connection
    :rtype session: AsyncSession
    """
    session: Optional[AsyncSession] = None
    async for session in get_db():
        break
    if session is None:
        raise RuntimeError("No database session available")
    return session
