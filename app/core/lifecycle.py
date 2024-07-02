"""
A module for lifecycle in the app-core package.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.db.init_db import init_db

logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[Any, None]:
    """
    The lifespan of the application
    :param application: The FastAPI application
    :type application: FastAPI
    :return: An asynchronous generator for the application
    :rtype: AsyncGenerator[Any, None]
    """
    logger.info("Starting API...")
    try:
        await init_db()
        yield
    except Exception as exc:
        logger.error(f"Error during application startup: {exc}")
        raise
    finally:
        logger.info("Application shutdown completed.")
