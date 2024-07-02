"""
Initialization of the database (PostgreSQL) script
"""

import logging
from typing import Union

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
    # TODO: Create super user using Mutation (GraphQL)


# Fictional data from dummy database on disk
employers: list[dict[str, Union[int, str]]] = [
    {
        "id": 1,
        "name": "MetaTechA",
        "contact_email": "contact@company-a.com",
        "industry": "Tech",
    },
    {
        "id": 2,
        "name": "MoneySoftB",
        "contact_email": "contact@company-b.com",
        "industry": "Finance",
    },
]
jobs: list[dict[str, Union[int, str]]] = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Develop web applications",
        "employer_id": 1,
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "description": "Analyze data and create reports",
        "employer_id": 1,
    },
    {
        "id": 3,
        "title": "Accountant",
        "description": "Manage financial records",
        "employer_id": 2,
    },
]
