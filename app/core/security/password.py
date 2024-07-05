"""
A module for password in the app.core.security package.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password_hasher: PasswordHasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a password using argon2.
    :param password: Plain text password.
    :return: Hashed password.
    """
    return password_hasher.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """
    Verify a password against the given hash.
    :param hashed_password: Hashed password.
    :param password: Plain text password.
    :return: True if password matches the hash, False otherwise.
    """
    try:
        return password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
