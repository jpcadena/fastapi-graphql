"""
This module handles JSON Web Token (JWT) creation for authentication
 and authorization.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from authlib.jose import JoseError
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.api.graphql.schemas.external.token import TokenPayload
from app.api.graphql.schemas.infrastructure.scope import Scope
from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings, get_init_settings
from app.config.init_settings import InitSettings
from app.utils.security.jwt import encode_jwt

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


def create_access_token(
    token_payload: TokenPayload,
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    init_settings: Annotated[InitSettings, Depends(get_init_settings)],
    scope: Scope = Scope.ACCESS_TOKEN,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a new JWT access token
    :param token_payload: The payload or claims for the token
    :type token_payload: TokenPayload
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :param init_settings: Dependency method for cached setting object
    :type init_settings: InitSettings
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
    try:
        header: dict[str, str] = {"alg": auth_settings.ALGORITHM}
        encoded_jwt: str = encode_jwt(
            header, payload, auth_settings, init_settings.ENCODING
        )
    except JoseError as exc:
        logger.error(f"JWT encoding error: {exc}")
        raise
    logger.info("JWT created with JTI: %s", token_payload.jti)
    return encoded_jwt


def create_refresh_token(
    token_payload: TokenPayload,
    auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
    init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> str:
    """
    Create a refresh token for authentication
    :param token_payload: The data to be used as payload in the token
    :type token_payload: TokenPayload
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :param init_settings: Dependency method for cached setting object
    :type init_settings: InitSettings
    :return: The access token with refresh expiration time
    :rtype: str
    """
    expires: timedelta = timedelta(
        minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    token: str = create_access_token(
        token_payload=token_payload,
        auth_settings=auth_settings,
        init_settings=init_settings,
        scope=Scope.REFRESH_TOKEN,
        expires_delta=expires,
    )
    return token
