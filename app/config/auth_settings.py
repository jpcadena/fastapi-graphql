"""
A module for auth settings in the app.core.config package.
"""

from typing import Optional

from pydantic import AnyHttpUrl, PositiveInt, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """
    Settings class for authentication using JWT and Redis
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    MAX_REQUESTS: PositiveInt = 30
    RATE_LIMIT_DURATION: PositiveInt = 60
    BLACKLIST_EXPIRATION_SECONDS: PositiveInt = 3600
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    TOKEN_URL: str = "api/v1/auth/login"
    TOKEN_USER_INFO_REGEX: str = (
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
        r"[0-9a-f]{4}-[0-9a-f]{12}:\d{1,3}\."
        r"\d{1,3}\.\d{1,3}\.\d{1,3}$"
    )
    SUB_REGEX: str = (
        r"^username:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
        r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )
    DETAIL: str = "Could not validate credentials"
    HEADERS: dict[str, str] = {"WWW-Authenticate": "Bearer"}
    SECRET_KEY: str
    SERVER_URL: AnyHttpUrl
    SERVER_DESCRIPTION: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    REFRESH_TOKEN_EXPIRE_MINUTES: PositiveInt
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: PositiveInt
    AUDIENCE: Optional[AnyHttpUrl] = None

    @field_validator("AUDIENCE", mode="before")
    def assemble_audience(
        cls, v: Optional[str], info: ValidationInfo
    ) -> AnyHttpUrl:
        """
        Combine server host and API_V1_STR to create the audience
        string.
        :param v: The value of audience attribute
        :type v: Optional[str]
        :param info: The field validation info
        :type info: ValidationInfo
        :return: The AUDIENCE attribute
        :rtype: AnyHttpUrl
        """
        # pylint: disable=unused-argument,no-self-argument,invalid-name
        if info.config is None:
            raise ValueError("info.config cannot be None")
        return AnyHttpUrl(
            f'{str(info.data.get("SERVER_URL"))[:-1]}:8000/'
            f'{info.data.get("TOKEN_URL")}'
        )
