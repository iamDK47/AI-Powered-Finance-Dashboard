"""Lazy PostgreSQL connection pool and FastAPI connection dependency."""

from collections.abc import Generator
from threading import Lock

from fastapi import HTTPException, status
from psycopg2 import Error as PsycopgError, OperationalError, pool

from app.api.core.config import settings

_pool: pool.ThreadedConnectionPool | None = None
_pool_lock = Lock()


def _get_pool() -> pool.ThreadedConnectionPool:
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                try:
                    _pool = pool.ThreadedConnectionPool(
                        minconn=1,
                        maxconn=10,
                        host=settings.db_host,
                        port=settings.db_port,
                        dbname=settings.db_name,
                        user=settings.db_user,
                        password=settings.db_password,
                        connect_timeout=5,
                    )
                except PsycopgError:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Database unavailable",
                    ) from None
    return _pool


def get_db() -> Generator:
    """Yield one pooled connection; database initialization stays lazy."""
    db_pool = _get_pool()
    try:
        connection = db_pool.getconn()
    except (PsycopgError, pool.PoolError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from None
    try:
        yield connection
    finally:
        db_pool.putconn(connection)
