"""Analytics response schemas."""

from pydantic import BaseModel


class PctChangePoint(BaseModel):
    date: str
    values: dict[str, float]


class VolatilityPoint(BaseModel):
    date: str
    volatility: float


class CorrelationMatrix(BaseModel):
    tickers: list[str]
    values: list[list[float]]
