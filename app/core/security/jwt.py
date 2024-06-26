"""
This module handles JSON Web Token (JWT) creation for authentication
 and authorization.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from jose import jwt

from app.api.graphql.schemas.external.token import TokenPayload
from app.api.graphql.schemas.infrastructure.scope import Scope
from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings

logger: logging.Logger = logging.getLogger(__name__)


def _generate_expiration_time(
    expires_delta: Optional[timedelta], minutes: Optional[float] = None
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
        return datetime.utcnow() + expires_delta
    if minutes is not None:
        return datetime.utcnow() + timedelta(minutes=minutes)
    value_error: ValueError = ValueError(
        "Either 'expires_delta' or 'minutes' must be provided."
    )
    logger.warning(value_error)
    raise value_error


def create_access_token(
    payload: TokenPayload,
    scope: Scope = Scope.ACCESS_TOKEN,
    expires_delta: Optional[timedelta] = None,
    auth_settings: AuthSettings = Depends(get_auth_settings),
) -> str:
    """
    Create a new JWT access token
    :param scope: The token's scope.
    :type scope: Scope
    :param payload: The payload or claims for the token
    :type payload: TokenPayload
    :param expires_delta: The timedelta specifying when the token should expire
    :type expires_delta: timedelta
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :return: The encoded JWT
    :rtype: str
    """
    claims: dict[str, Any]
    if expires_delta:
        expire_time: datetime = _generate_expiration_time(
            expires_delta, auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        updated_payload: TokenPayload = payload.model_copy(
            update={"exp": int(expire_time.timestamp()), "scope": scope}
        )
        claims = jsonable_encoder(updated_payload)
    else:
        claims = jsonable_encoder(payload)
    encoded_jwt: str = jwt.encode(
        claims=claims,
        key=auth_settings.SECRET_KEY,
        algorithm=auth_settings.ALGORITHM,
    )
    logger.info("JWT created with JTI: %s", payload.jti)
    return encoded_jwt


def create_refresh_token(
    payload: TokenPayload,
    auth_settings: AuthSettings = Depends(get_auth_settings),
) -> str:
    """
    Create a refresh token for authentication
    :param payload: The data to be used as payload in the token
    :type payload: TokenPayload
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :return: The access token with refresh expiration time
    :rtype: str
    """
    expires: timedelta = timedelta(
        minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    token: str = create_access_token(
        payload=payload,
        scope=Scope.REFRESH_TOKEN,
        expires_delta=expires,
        auth_settings=auth_settings,
    )
    return token
