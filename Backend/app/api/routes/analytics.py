"""Daily price performance and risk analytics."""

from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.api.database.connection import get_db
from app.api.schemas.analytics import CorrelationMatrix, PctChangePoint, VolatilityPoint
from app.api.services.analytics_service import correlation, pct_change, volatility
from app.api.services.market_services import fetch_klines

router = APIRouter(prefix="/analytics", tags=["analytics"])


def _fetch_window(connection, ticker: str | None, start: datetime | None, end: datetime | None, limit: int):
    if ticker:
        return fetch_klines(connection, ticker.upper(), start, end, limit)
    # Use known ticker list to reuse the same safe, parameterized candle query.
    from app.api.services.market_services import fetch_tickers

    rows = []
    for symbol in fetch_tickers(connection):
        rows.extend(fetch_klines(connection, symbol, start, end, limit))
    return rows


@router.get("/performance", response_model=list[PctChangePoint])
def performance(
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(5000, ge=1, le=5000),
    connection=Depends(get_db),
):
    """Return daily percent changes from the first shared date, by ticker."""
    return pct_change(_fetch_window(connection, None, start, end, limit))


@router.get("/volatility", response_model=list[VolatilityPoint])
def get_volatility(
    ticker: str = Query(..., min_length=1, max_length=32),
    window: int = Query(7, ge=2, le=90),
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(5000, ge=1, le=5000),
    connection=Depends(get_db),
):
    """Return rolling daily return volatility, expressed as a percentage."""
    rows = _fetch_window(connection, ticker, start, end, limit)
    return volatility(rows, ticker.upper(), window)


@router.get("/correlation", response_model=CorrelationMatrix)
def get_correlation(
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = Query(5000, ge=1, le=5000),
    connection=Depends(get_db),
) -> CorrelationMatrix:
    """Return the Pearson correlation matrix for daily asset returns."""
    return correlation(_fetch_window(connection, None, start, end, limit))
