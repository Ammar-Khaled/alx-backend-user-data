#!/usr/bin/env python3
"""encript password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """converts input string password to unicode,
    then returns salted, hashed pswd as bytestring."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
