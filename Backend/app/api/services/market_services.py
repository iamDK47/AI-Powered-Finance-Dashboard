"""Market-data database operations."""

from datetime import datetime

from fastapi import HTTPException, status
from psycopg2 import Error as PsycopgError
from psycopg2.extras import RealDictCursor

from app.api.database.queries import KLINES_QUERY, TICKERS_QUERY


def fetch_klines(
    connection,
    ticker: str,
    start: datetime | None,
    end: datetime | None,
    limit: int,
) -> list[dict]:
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(KLINES_QUERY, (ticker, start, start, end, end, limit))
            return [dict(row) for row in cursor.fetchall()]
    except PsycopgError:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not read market data",
        ) from None


def fetch_tickers(connection) -> list[str]:
    try:
        with connection.cursor() as cursor:
            cursor.execute(TICKERS_QUERY)
            return [row[0] for row in cursor.fetchall()]
    except PsycopgError:
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not read market data",
        ) from None
