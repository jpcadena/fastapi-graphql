"""
A module for jwt in the app.utils.security package.
"""

import logging
from typing import Any

from fastapi import Depends, HTTPException, status
from jose import exceptions, jwt
from pydantic import ValidationError

from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings

logger: logging.Logger = logging.getLogger(__name__)
headers: dict[str, str] = {"WWW-Authenticate": "Bearer"}
detail: str = "Could not validate credentials"


def encode_jwt(
    payload: dict[str, Any],
    auth_settings: AuthSettings = Depends(get_auth_settings),
) -> str:
    """
    Encode a JSON Web Token (JWT) with the given payload.
    :param payload: The payload to encode
    :type payload: dict[str, Any]
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :return: The JSON Web Token
    :rtype: str
    """
    return jwt.encode(
        payload, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
    )


def decode_jwt(
    token: str, auth_settings: AuthSettings = Depends(get_auth_settings)
) -> dict[str, Any]:
    """
    Validate the provided JWT token.
    :param token: JWT token to be validated
    :type token: str
    :param auth_settings: Dependency method for cached setting object
    :type auth_settings: AuthSettings
    :return: Decoded payload of the valid JWT token
    :rtype: dict[str, Any]
    """
    try:
        return jwt.decode(
            token=token,
            key=auth_settings.SECRET_KEY,
            algorithms=[auth_settings.ALGORITHM],
            options={"verify_subject": False},
            audience=str(auth_settings.AUDIENCE),
            issuer=str(auth_settings.SERVER_URL),
        )
    except exceptions.ExpiredSignatureError as es_exc:
        logger.error(es_exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers=headers,
        ) from es_exc
    except exceptions.JWTClaimsError as c_exc:
        logger.error(c_exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization claim is incorrect,"
            " please check audience and issuer",
            headers=headers,
        ) from c_exc
    except (exceptions.JWTError, ValidationError) as exc:
        logger.error(exc)
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail, headers) from exc
