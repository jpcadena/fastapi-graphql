"""
A module for feature in the app.schemas.infrastructure package.
"""

from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class Feature(StrEnum):
    """
    Enum representing different feature options
    """

    EYE = auto()
    NOSE = auto()
    MOUTH = auto()
