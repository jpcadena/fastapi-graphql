"""
A module for lifecycle in the app-core package.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.config import init_setting, setting
from app.db.init_db import init_db

logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager  # type: ignore
async def lifespan(application: FastAPI) -> None:
    """
    The lifespan of the application
    :param application: The FastAPI application
    :type application: FastAPI
    :return: An asynchronous generator for the application
    :rtype: AsyncGenerator[Any, None]
    """
    logger.info("Starting API...")
    await init_db(setting, init_setting)
