"""
A module for scope in the app.schemas.infrastructure package.
"""

from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class Scope(StrEnum):
    """
    Enum representing different scopes
    """

    ACCESS_TOKEN = auto()
    REFRESH_TOKEN = auto()
