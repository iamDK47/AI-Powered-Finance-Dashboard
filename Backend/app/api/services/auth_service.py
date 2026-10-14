"""Credential validation and token creation."""

from fastapi import HTTPException, status

from app.api.core.config import settings
from app.api.core.security import create_access_token, verify_password


def authenticate(username: str, password: str) -> str:
    valid_user = username == settings.admin_username
    valid_password = valid_user and verify_password(
        password, settings.admin_password_hash
    )
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_access_token(username)
