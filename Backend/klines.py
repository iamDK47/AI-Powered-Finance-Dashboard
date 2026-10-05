from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

from app.database import get_db
from app.schemas import KlineOut
from app.security import get_current_user

router = APIRouter(prefix="/klines", tags=["klines"])


@router.get("", response_model=list[KlineOut])
def get_klines(
    ticker: str = Query(..., description="e.g. BTCUSDT"),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(1000, le=5000),
    # Auth dependency declared BEFORE the database dependency, on purpose:
    # FastAPI resolves Depends() in the order they're listed here. An
    # unauthenticated request should be rejected immediately — before
    # spending a database connection on it, and before it can learn
    # anything about the database's status at all (imagine a caller with
    # no token learning "database unavailable" — that's telling a
    # stranger something true about your infrastructure for free). Get
    # this ordering backwards and an unauthed caller can get a 503
    # instead of a 401, which is exactly the bug this comment is here to
    # stop you from reintroducing.
    current_user: str = Depends(get_current_user),
    conn=Depends(get_db),
):
    # Parameterized query — %s placeholders, values passed separately,
    # same pattern your own load_kline already uses. Never do
    # f"WHERE ticker = '{ticker}'" — that's exactly how SQL injection
    # happens, and it's not a theoretical risk once this is reachable
    # from the public internet instead of just your own script.
    query = "SELECT * FROM global_crypto_data WHERE ticker = %s"
    params: list = [ticker]

    if start:
        query += " AND open_time >= %s"
        params.append(start)
    if end:
        query += " AND open_time <= %s"
        params.append(end)

    query += " ORDER BY open_time ASC LIMIT %s"
    params.append(limit)

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
    except OperationalError:
        # Postgres unreachable/down — tell the client clearly instead of
        # letting a raw psycopg2 traceback leak back to the frontend.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        )

    return rows
