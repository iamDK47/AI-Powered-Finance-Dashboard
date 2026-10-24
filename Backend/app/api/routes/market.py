"""Market candle and ticker endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from app.api.database.connection import get_db
from app.api.schemas.market import KlineOut, TickerList
from app.api.services.market_services import fetch_klines, fetch_tickers

router = APIRouter(tags=["market"])


@router.get("/klines", response_model=list[KlineOut])
def get_klines(
    ticker: str,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int = 1000,
    connection=Depends(get_db),
):
    """Return oldest-first candles for one symbol."""
    if start and end and start > end:
        raise HTTPException(status_code=422, detail="start must be before end")
    return fetch_klines(connection, ticker.upper(), start, end, limit)


@router.get("/tickers", response_model=TickerList)
def get_tickers(
    connection=Depends(get_db),
):
    """Return symbols present in the market-data table."""
    return TickerList(tickers=fetch_tickers(connection))
