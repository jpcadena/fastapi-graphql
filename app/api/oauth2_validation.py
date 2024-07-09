"""
A module for oauth2 validation in the app.api package.
"""

import logging
from functools import wraps
from typing import Any, Callable

from graphql import GraphQLError, GraphQLResolveInfo
from pydantic import PositiveInt
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.graphql.resolvers.user import resolver_user
from app.config.auth_settings import AuthSettings
from app.config.config import auth_setting
from app.db.session import get_session
from app.exceptions.exceptions import (
    DatabaseException,
    NotFoundException,
    raise_unauthorized_error,
)
from app.models.user import User
from app.schemas.external.user import UserAuth
from app.utils.security.jwt import decode_jwt

logger: logging.Logger = logging.getLogger(__name__)


async def get_login_user(username: str) -> User:
    """
    Retrieve user information for login purposes by its username
    :param username: The username to retrieve User from
    :type username: str
    :return: User information
    :rtype: User
    """
    stmt: Select[Any]
    async_session: AsyncSession = await get_session()
    stmt = select(User).where(User.username == username)
    try:
        user: User | None = (await async_session.scalars(stmt)).first()
    except SQLAlchemyError as sa_exc:
        raise DatabaseException(str(sa_exc)) from sa_exc
    if not user:
        raise NotFoundException(f"User not found with username: {username}")
    return user


async def authenticate_user(
    token: str,
    auth_settings: AuthSettings,
) -> UserAuth:
    """
    Authenticates a user based on the provided token (access or refresh token)
    :param token: JWT token from OAuth2PasswordBearer
    :type token: str
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :return: Authenticated user information
    :rtype: UserAuth
    """
    payload: dict[str, Any] = decode_jwt(token, auth_settings)
    username: str = payload.get("preferred_username")  # type: ignore
    sub: str = payload.get("sub")  # type: ignore
    if not username or not sub:
        await raise_unauthorized_error(
            auth_settings.DETAIL, auth_settings.HEADERS
        )
    user: User = await get_login_user(username)
    user_auth: UserAuth = UserAuth.model_validate(user)
    return user_auth


def admin_user(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator validates the role of the user to be admin
    :param func: The function to be decorated
    :type func: Callable
    :return: The decorated function that validates if the user is an admin
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        A wrapper function that authenticates the user and authorizes the
        user if its admin to perform another action
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: tuple[Any, ...]
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: dict[str, Any]
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        if len(args) < 2 or not isinstance(args[1], GraphQLResolveInfo):
            raise GraphQLError("No information available")
        info: GraphQLResolveInfo = args[1]
        user_auth: UserAuth = await authenticate_user(
            info.context, auth_setting
        )
        user: User = await resolver_user(user_auth.id)
        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")
        value = await func(*args, **kwargs)
        return value

    return wrapper


async def auth_user(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator validates the user as logged in
    :param func: The function to be decorated
    :type func: Callable
    :return: The decorated function that validates if the user is an admin
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        A wrapper function that authenticates the user
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: tuple[Any, ...]
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: dict[str, Any]
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        if len(args) < 2 or not isinstance(args[1], GraphQLResolveInfo):
            raise GraphQLError("No information available")
        info: GraphQLResolveInfo = args[1]
        user_auth: UserAuth = await authenticate_user(
            info.context, auth_setting
        )
        value = await func(*args, **kwargs)
        return value

    return wrapper


def auth_same_user(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator validates that the user is the same as the authenticated
    :param func: The function to be decorated
    :type func: Callable
    :return: The decorated function that validates if the user is an admin
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        A wrapper function that authenticates the user to be the same
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: tuple[Any, ...]
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: dict[str, Any]
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        if len(args) < 2 or not isinstance(args[1], GraphQLResolveInfo):
            raise GraphQLError("No information available")
        info: GraphQLResolveInfo = args[1]
        user_auth: UserAuth = await authenticate_user(
            info.context, auth_setting
        )
        user_id: PositiveInt | None = kwargs.get("user_id")
        if user_id is None:
            raise GraphQLError("No user ID provided")
        if user_auth.id != user_id:
            raise GraphQLError("You are not authorized to perform this action")
        value = await func(*args, **kwargs)
        return value

    return wrapper
