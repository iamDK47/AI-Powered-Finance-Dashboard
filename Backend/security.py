from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import settings

# This tells FastAPI's auto-generated /docs page where to send a login
# request from its "Authorize" button. It does NOT enforce anything by
# itself — get_current_user below is what actually checks the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def create_access_token(subject: str) -> str:
    """Builds a JWT: a signed, tamper-evident string encoding who this is
    (`sub`) and when it expires (`exp`). Signed with your secret key, so
    anyone holding the key can verify it wasn't forged or edited — but the
    token itself isn't encrypted, so never put sensitive data inside it."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Route dependency that verifies the JWT sent in the Authorization
    header. Notice there's no database lookup here at all — checking the
    signature IS the verification. That's what "stateless" auth means:
    the server doesn't need to remember anything about active sessions,
    the token carries its own proof.

    Add `current_user: str = Depends(get_current_user)` as a parameter to
    ANY route, and FastAPI runs this before the route body — the route
    never executes at all if the token is missing, expired, or invalid."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        # Covers a bad signature (tampered/forged token), a malformed
        # token, AND an expired one — jose raises this same exception type
        # for all three, so one except block correctly catches all of them.
        raise credentials_exception
