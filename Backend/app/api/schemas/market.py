"""Market-data response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class KlineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class TickerList(BaseModel):
    tickers: list[str]
