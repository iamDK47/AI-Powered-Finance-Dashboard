from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class KlineOut(BaseModel):
    """Shape of one row returned by GET /klines. Listing every field here
    isn't decoration — FastAPI uses this to validate every outgoing row
    against these exact types BEFORE sending it, and to auto-generate the
    request/response docs at /docs. If a query ever returns a row missing
    a field or with a wrong type, you get a clear 500 error pointing at
    the mismatch, instead of the frontend silently receiving bad data."""

    ticker: str
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    coin_volume: float
    quote_asset_volume: float
    total_trades: int
    market_buy_volume: float
    market_buy_quote_volume: float
    delta: float
    close_time: datetime
