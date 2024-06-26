"""
A module for json utils in the app.utils.files utils package.
"""

import json
import logging
from typing import Any

import aiofiles
from fastapi import Depends

from app.config.config import get_init_settings
from app.config.init_settings import InitSettings
from app.core.decorators import benchmark, with_logging

logger: logging.Logger = logging.getLogger(__name__)


@with_logging
@benchmark
async def read_json_file(
    init_setting: InitSettings = Depends(get_init_settings),
) -> dict[str, Any]:
    """
    Read the OpenAPI JSON file
    :param init_setting: Dependency method for cached setting object
    :type init_setting: InitSettings
    :return: JSON data
    :rtype: dict[str, Any]
    """
    file_path: str = f"{init_setting.OPENAPI_FILE_PATH}"
    async with aiofiles.open(
        file_path, mode="r", encoding=init_setting.ENCODING
    ) as file:
        content = await file.read()
        logger.info("Json file read: %s", file_path)
    if not content:
        raise ValueError(f"The file {file_path} is empty or not readable.")
    data: dict[str, Any] = json.loads(content)
    return data


@with_logging
@benchmark
async def write_json_file(
    data: dict[str, Any],
    init_setting: InitSettings = Depends(get_init_settings),
) -> None:
    """
    Write the modified JSON data back to the file
    :param data: Modified JSON data
    :type data: dict[str, Any]
    :param init_setting: Dependency method for cached setting object
    :type init_setting: InitSettings
    :return: None
    :rtype: NoneType
    """
    file_path: str = f"{init_setting.OPENAPI_FILE_PATH}"
    async with aiofiles.open(
        file_path, mode="w", encoding=init_setting.ENCODING
    ) as out_file:
        await out_file.write(json.dumps(data, indent=4))
    logger.info("Json file written: %s", init_setting.OPENAPI_FILE_PATH)
