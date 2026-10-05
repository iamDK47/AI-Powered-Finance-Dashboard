from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings
from app.schemas import Token
from app.security import create_access_token, verify_password

# APIRouter is FastAPI's version of a controller grouping: every route
# declared on `router` gets this prefix and tag automatically. main.py
# then does app.include_router(router) once, instead of you registering
# each endpoint individually on the main app object.
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2PasswordRequestForm expects FORM-encoded username/password —
    not a JSON body. This is the standard OAuth2 convention (and what
    makes the /docs page's built-in "Authorize" button work without any
    extra code). Your Next.js client needs to send this as
    application/x-www-form-urlencoded, not JSON.stringify — see api.ts,
    this is the single most common place people get stuck first."""
    valid_user = form_data.username == settings.admin_username
    valid_password = valid_user and verify_password(
        form_data.password, settings.admin_password_hash
    )

    if not valid_password:
        # Deliberately the SAME error for "wrong username" and "wrong
        # password" — telling an attacker which one was wrong narrows
        # their search space for free. Never distinguish the two.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(subject=form_data.username)
    return Token(access_token=access_token)
