"""
A module for openapi utils in the app.utils.files utils package.
"""

import json
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.config.config import auth_setting, init_setting, setting


def remove_tag_from_operation_id(tag: str, operation_id: str) -> str:
    """
    Remove tag from the operation ID
    :param tag: Tag to remove
    :type tag: str
    :param operation_id: Original operation ID
    :type operation_id: str
    :return: Updated operation ID
    :rtype: str
    """
    return operation_id.removeprefix(f"{tag}-")


def update_operation_id(operation: dict[str, Any]) -> None:
    """
    Update the operation ID of a single operation.
    :param operation: Operation object
    :type operation: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    tag: str = operation["tags"][0]
    operation_id: str = operation["operationId"]
    new_operation_id: str = remove_tag_from_operation_id(tag, operation_id)
    operation["operationId"] = new_operation_id


def modify_json_data(
    data: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Modify the JSON data
    :param data: JSON data to modify
    :type data: dict[str, Any]
    :return: Modified JSON data
    :rtype: dict[str, Any]
    """
    paths: Optional[dict[str, dict[str, dict[str, Any]]]] = data.get("paths")
    if not paths:
        return data
    for key, path_data in paths.items():
        if key == "/":
            continue
        for operation in dict(path_data).values():
            update_operation_id(operation)
    return data


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Generate a custom unique ID for each route in API
    :param route: endpoint route
    :type route: APIRoute
    :return: new ID based on tag and route name
    :rtype: str
    """
    if route.name in ("redirect_to_docs",):
        return ""
    return f"{route.tags[0]}-{route.name}"


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """
    Generate a custom OpenAPI schema for the application.
    This function customizes the default FastAPI OpenAPI generation by
    incorporating additional configuration settings and modifying the schema.
    The modified schema is then cached for subsequent requests.
    :param app: FastAPI instance.
    :type app: FastAPI
    :return: Customized OpenAPI schema.
    :rtype: dict[str, Any]
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema: dict[str, Any] = get_openapi(
        title=init_setting.PROJECT_NAME,
        version=init_setting.VERSION,
        summary=init_setting.SUMMARY,
        description=init_setting.DESCRIPTION,
        routes=app.routes,
        servers=[
            {
                "url": auth_setting.SERVER_URL,
                "description": auth_setting.SERVER_DESCRIPTION,
            }
        ],
        contact=setting.CONTACT,
        license_info=init_setting.LICENSE_INFO,
    )
    openapi_schema = modify_json_data(openapi_schema)
    app.openapi_schema = openapi_schema
    file_path: str = f"{init_setting.OPENAPI_FILE_PATH}"[1:]
    with open(file_path, mode="w", encoding=init_setting.ENCODING) as out_file:
        out_file.write(json.dumps(openapi_schema, indent=4))
    return app.openapi_schema
