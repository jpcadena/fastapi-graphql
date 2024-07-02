"""
A module for sql database settings in the app.core.config package.
"""

from typing import Optional

from pydantic import PositiveInt, PostgresDsn, field_validator
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLDatabaseSettings(BaseSettings):
    """
    Settings class for SQL database configuration
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )
    TIMESTAMP_PRECISION: PositiveInt = 2
    DB_EMAIL_CONSTRAINT: str = (
        "contact_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\"
        ".[A-Z|a-z]{2,"
        "}$'"
    )
    POSTGRES_SCHEME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_postgresql_connection(
        cls, v: Optional[str], info: ValidationInfo
    ) -> PostgresDsn:
        """
        Assemble the database connection as URI string
        :param v: Variables to consider
        :type v: str
        :param info: The field validation info
        :type info: ValidationInfo
        :return: SQLAlchemy URI
        :rtype: PostgresDsn
        """
        # pylint: disable=no-self-argument,invalid-name
        if info.config is None:
            raise ValueError("info.config cannot be None")
        uri: MultiHostUrl = MultiHostUrl.build(
            scheme=info.data.get("POSTGRES_SCHEME", "postgresql"),
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_HOST"),
            port=info.data.get("POSTGRES_PORT"),
            path=info.data.get("POSTGRES_DB"),
            # query="ssl=require",
        )
        return PostgresDsn(str(uri))
