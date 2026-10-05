from contextlib import contextmanager
from typing import Optional

from fastapi import HTTPException, status
from psycopg2 import OperationalError, pool

from app.config import settings

_pool: Optional[pool.ThreadedConnectionPool] = None


def _get_pool() -> pool.ThreadedConnectionPool:
    """Built on FIRST USE, not at import time. Creating it eagerly at
    import would mean the whole app fails to start whenever Postgres
    isn't reachable yet — including routes like /health that never touch
    the database at all. Lazy creation means only requests that actually
    need the database are affected if Postgres is down."""
    global _pool
    if _pool is None:
        _pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
        )
    return _pool


@contextmanager
def get_connection():
    try:
        db_pool = _get_pool()
        conn = db_pool.getconn()
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )
    try:
        yield conn
    finally:
        db_pool.putconn(conn)


def get_db():
    """FastAPI dependency — add `conn = Depends(get_db)` to any route that
    needs the database."""
    with get_connection() as conn:
        yield conn
