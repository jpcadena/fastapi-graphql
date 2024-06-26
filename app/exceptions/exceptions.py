"""
This module defines custom exception classes for the Core Security
"""

from typing import Optional

from sqlalchemy.exc import SQLAlchemyError


class DatabaseException(SQLAlchemyError):
    """
    Database Exception class
    """

    def __init__(self, message: str, note: Optional[str] = None):
        super().__init__(message)
        if note:
            self.add_note(note)


class ServiceException(Exception):
    """
    Service Layer Exception class
    """

    def __init__(self, message: str, note: Optional[str] = None):
        super().__init__(message)
        if note:
            self.add_note(note)


class NotFoundException(Exception):
    """
    Not Found Exception class
    """

    def __init__(self, message: str, note: Optional[str] = None):
        super().__init__(message)
        if note:
            self.add_note(note)


class SecurityException(Exception):
    """
    Security Exception class
    """

    def __init__(self, message: str, note: Optional[str] = None):
        super().__init__(message)
        if note:
            self.add_note(note)


class GeolocationError(Exception):
    """Custom exception for Geolocation related errors."""


class QueryLimitExceeded(GeolocationError):
    """Raised when the query limit for the Maps API is exceeded."""


class UnsupportedFileTypeError(Exception):
    """Raised when the file type is not supported"""


class FileSizeExceededError(Exception):
    """Raised when the file size exceeds the maximum in MB"""


class VideoDurationExceededError(Exception):
    """Raised when the video duration exceeds the maximum in seconds."""
