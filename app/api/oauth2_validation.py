"""
A module for oauth2 validation in the app.api package.
"""

from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.auth_settings import AuthSettings
from app.db.session import get_session
from app.exceptions.exceptions import (
    DatabaseException,
    NotFoundException,
    raise_unauthorized_error,
)
from app.models.user import User
from app.schemas.external.user import UserAuth
from app.utils.security.jwt import decode_jwt


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
