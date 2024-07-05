"""
Initialization of the database (PostgreSQL) script
"""

import logging
from typing import Any

from sqlalchemy.exc import (
    CompileError,
    DatabaseError,
    DataError,
    DisconnectionError,
    IntegrityError,
    InternalError,
    InvalidatePoolError,
    PendingRollbackError,
)
from sqlalchemy.exc import TimeoutError as SATimeoutError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncTransaction

from app.core.decorators import benchmark, with_logging
from app.core.security.password import hash_password
from app.db.base_class import Base
from app.db.dummy_data import applications, employers, jobs, users
from app.db.session import async_engine, get_session
from app.models import __all__ as tables
from app.models.application import Application
from app.models.employer import Employer
from app.models.job import Job
from app.models.user import User

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
@benchmark
async def create_db_and_tables() -> None:
    """
    Create the database and tables if they don't exist
    :return: None
    :rtype: NoneType
    """
    async with async_engine.connect() as async_connection:
        try:
            async_transaction: AsyncTransaction = async_connection.begin()
            await async_transaction.start()
            await async_connection.run_sync(Base.metadata.drop_all)
            for table in tables:
                await async_connection.run_sync(
                    table.__table__.create  # type: ignore
                )
            await async_transaction.commit()
        except (
            PendingRollbackError,
            CompileError,
            DataError,
            IntegrityError,
            InternalError,
            DatabaseError,
            InvalidatePoolError,
            DisconnectionError,
            SATimeoutError,
        ) as exc:
            await async_transaction.rollback()
            logger.error(exc)


async def bulk_insert(
    session: AsyncSession,
    model: type[Base],  # type: ignore
    data: list[dict[str, Any]],
) -> None:
    """
    Bulk insert data into the database.
    :param session: The database session
    :param model: The model class
    :param data: The data to insert
    :return: None
    :rtype: NoneType
    """
    try:
        await session.execute(model.__table__.insert(), data)  # type: ignore
    except Exception as exc:
        logger.error(f"Error inserting data into {model.__name__}: {exc}")


@with_logging
@benchmark
async def init_db() -> None:
    """
    Initialize the database connection and create the necessary tables.
    :return: None
    :rtype: NoneType
    """
    await create_db_and_tables()
    async_session: AsyncSession = await get_session()
    for user in users:
        user["hashed_password"] = hash_password(user.pop("password"))
    await bulk_insert(async_session, Employer, employers)
    await bulk_insert(async_session, Job, jobs)
    await bulk_insert(async_session, User, users)
    await bulk_insert(async_session, Application, applications)
    await async_session.commit()
    await async_session.close()
