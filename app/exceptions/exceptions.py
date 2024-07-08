"""
This module defines custom exception classes for the Core Security
"""

from typing import Any, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


class DatabaseException(SQLAlchemyError):  # type: ignore
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


class UnauthorizedError(HTTPException):  # type: ignore
    def __init__(self, detail: str, headers: dict[str, Any]):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


async def raise_unauthorized_error(
    detail: str, headers: dict[str, Any]
) -> None:
    """
    Raises an UnauthorizedError exception.
    :param detail: Detailed message for the unauthorized error.
    :type detail: str
    :param headers: Headers to be included in the HTTP response.
    :type headers: dict[str, Any]
    :return: None
    :rtype: NoneType
    """
    raise UnauthorizedError(detail, headers)
