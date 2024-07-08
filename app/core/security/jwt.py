"""
This module handles JSON Web Token (JWT) creation for authentication
 and authorization.
"""

import logging
import time
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from authlib.jose import JoseError, jwt
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings
from app.models.user import User
from app.schemas.external.token import TokenPayload
from app.schemas.infrastructure.scope import Scope

logger: logging.Logger = logging.getLogger(__name__)


def _generate_expiration_time(
    expires_delta: timedelta | None, minutes: float | None = None
) -> datetime:
    """
    Generate an expiration time for JWT
    :param expires_delta: The timedelta specifying when the token
     should expire
    :type expires_delta: timedelta
    :param minutes: The minutes to add to the current time to get the
     expiration time
    :type minutes: float
    :return: The calculated expiration time
    :rtype: datetime
    """
    if expires_delta:
        return datetime.now(UTC) + expires_delta
    if minutes is not None:
        return datetime.now(UTC) + timedelta(minutes=minutes)
    value_error: ValueError = ValueError(
        "Either 'expires_delta' or 'minutes' must be provided."
    )
    logger.warning(value_error)
    raise value_error


def build_payload(
    user: User,
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    scope: Scope | None = None,
) -> TokenPayload:
    """
    Build JWT payload for authentication
    :param user: User to authenticate
    :type user: User
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :param scope: The scope for the token creation. Default value is None
    :type scope: Scope
    :return: Payload for JWT
    :rtype: TokenPayload
    """
    current_time: int = int(time.time())
    access_expiration_time: int = current_time + int(
        auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    refresh_expiration_time: int = current_time + int(
        auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )
    expiration_time: int = (
        access_expiration_time
        if scope != Scope.REFRESH_TOKEN
        else refresh_expiration_time
    )
    user_data: dict[str, Any] = {
        "sub": f"username:{str(user.id)}",
        "email": user.email,
        "nickname": user.username,
        "preferred_username": user.username,
        "updated_at": user.updated_at,
        "exp": expiration_time,
        "nbf": current_time - 1,
        "iat": current_time,
    }
    if scope:
        user_data["scope"] = scope
    return TokenPayload(**user_data)


def create_access_token(
    token_payload: TokenPayload,
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    scope: Scope = Scope.ACCESS_TOKEN,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a new JWT access token
    :param token_payload: The payload or claims for the token
    :type token_payload: TokenPayload
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :param scope: The token's scope.
    :type scope: Scope
    :param expires_delta: The timedelta specifying when the token should expire
    :type expires_delta: timedelta
    :return: The encoded JWT
    :rtype: str
    """
    payload: dict[str, Any]
    if expires_delta:
        expire_time: datetime = _generate_expiration_time(
            expires_delta, auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        updated_payload: TokenPayload = token_payload.model_copy(
            update={"exp": int(expire_time.timestamp()), "scope": scope}
        )
        payload = jsonable_encoder(updated_payload)
    else:
        payload = jsonable_encoder(token_payload)
    header: dict[str, str] = {"alg": auth_settings.ALGORITHM}
    try:
        encoded_jwt: str = jwt.encode(header, payload, auth_settings.SECRET_KEY)
    except JoseError as exc:
        logger.error(f"JWT encoding error: {exc}")
        raise
    logger.info("JWT created with JTI: %s", token_payload.jti)
    return encoded_jwt
