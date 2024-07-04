"""
Initialization of the database (PostgreSQL) script
"""

import logging

from sqlalchemy.exc import (
    CompileError,
    DataError,
    DatabaseError,
    DisconnectionError,
    IntegrityError,
    InternalError,
    InvalidatePoolError,
    PendingRollbackError,
)
from sqlalchemy.exc import TimeoutError as SATimeoutError
from sqlalchemy.ext.asyncio import AsyncTransaction

from app.core.decorators import benchmark, with_logging
from app.db.base_class import Base
from app.db.session import async_engine
from app.models import __all__ as tables

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


@with_logging
@benchmark
async def init_db() -> None:
    """
    Initialize the database connection and create the necessary tables.
    :return: None
    :rtype: NoneType
    """
    await create_db_and_tables()
