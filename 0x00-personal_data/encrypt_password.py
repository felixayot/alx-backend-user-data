#!/usr/bin/env python3
"""Module for hash_password function."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypts a password using the bcrypt library."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a password is valid."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
