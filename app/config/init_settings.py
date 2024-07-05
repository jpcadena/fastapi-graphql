"""
A module for init settings in the app.core.config package.
"""

import base64
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_image_b64(image_path: str) -> str:
    """
    Converts an image to base64 format
    :param image_path: Path to the image file
    :type image_path: str
    :return: The image file in base64 format
    :rtype: str
    """
    return base64.b64encode(Path(image_path).read_bytes()).decode("utf")


img_b64: str = get_image_b64("assets/images/project.png")
users_b64: str = get_image_b64("assets/images/users.png")
auth_b64: str = get_image_b64("assets/images/auth.png")


class InitSettings(BaseSettings):
    """
    Init Settings class based on Pydantic Base Settings
    """

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="allow",
    )

    PROJECT_NAME: str = "fastapi-graphql"
    VERSION: str = "1.0"
    ENCODING: str = "UTF-8"
    OPENAPI_FILE_PATH: str = "/openapi.json"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    FILE_DATE_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
    IMAGES_APP: str = "images"
    IMAGES_PATH: str = "/assets/images"
    IMAGES_DIRECTORY: str = "assets/images"
    LOG_FORMAT: str = (
        "[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
        "[%(funcName)s][%(lineno)d]: %(message)s"
    )
    PASSWORD_REGEX: str = (
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?" "[#?!@$%^&*-]).{8,14}$"
    )
    SUMMARY: str = """
    This backend project is a FastAPI backend using GraphQL.
    """
    DESCRIPTION: str = f"""**FastAPI**, **SQLAlchemy** and **Graphene** helps
    you do awesome stuff. 🚀
    \n\n<img src="data:image/png;base64,{img_b64}"/>"""
    LICENSE_INFO: dict[str, str] = {
        "name": "MIT",
        "identifier": "MIT",
    }
    TAGS_METADATA: list[dict[str, str]] = [
        {
            "name": "user",
            "description": f"""Operations with users, such as register, get,
             update and delete.\n\n<img src="data:image/png;base64,
             {users_b64}" width="150" height="100"/>""",
        },
        {
            "name": "auth",
            "description": f"""The authentication logic is here as well as
             password recovery and reset.
             \n\n<img src="data:image/png;base64,{auth_b64}" width="75"
             height="75"/>""",
        },
    ]
