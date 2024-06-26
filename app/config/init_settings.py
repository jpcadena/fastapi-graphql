"""
A module for init settings in the app.core.config package.
"""

import base64
from pathlib import Path

from pydantic import HttpUrl, PositiveInt
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

    ITERATIONS: PositiveInt = 100000
    KEY_BYTES_LENGTH: PositiveInt = 32
    SALT_BYTES: PositiveInt = 16
    IV_BYTES: PositiveInt = 12
    PUBLIC_EXPONENT: PositiveInt = 65537
    RSA_KEY_BITS: PositiveInt = 2048
    SALUTE: str = "Salute!"
    ROOT_MSG: str = "Hello, World!"
    SERVER_NAME: str = "FastAPI GraphQL"
    PROJECT_NAME: str = "fastapi-graphql"
    VERSION: str = "1.0"
    ENCODING: str = "UTF-8"
    DEFAULT_REGION: str = "Guayas"
    DEFAULT_COUNTRY: str = "Ecuador"
    OPENAPI_FILE_PATH: str = "/openapi.json"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    FILE_DATE_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
    IMAGES_APP: str = "images"
    IMAGES_PATH: str = "/assets/images"
    IMAGES_DIRECTORY: str = "assets/images"
    EMAIL_TEMPLATES_DIR: str = "templates"
    PASSWORD_RECOVERY_SUBJECT: str = "Password recovery for user"
    NEW_ACCOUNT_SUBJECT: str = "New account for user"
    WELCOME_SUBJECT: str = "Welcome to "
    PASSWORD_CHANGED_CONFIRMATION_SUBJECT: str = (
        "Successfully password " "changed for "
    )
    DELETE_ACCOUNT_SUBJECT: str = "Account deleted for "
    LOG_FORMAT: str = (
        "[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
        "[%(funcName)s][%(lineno)d]: %(message)s"
    )
    PASSWORD_REGEX: str = (
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?" "[#?!@$%^&*-]).{8,14}$"
    )
    GOOGLE_MAPS_API_URL: HttpUrl = HttpUrl(
        "https://maps.googleapis.com/maps/api/geocode/json"
    )

    SUMMARY: str = """This backend project is a FastAPI backend in GraphQL."""
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
