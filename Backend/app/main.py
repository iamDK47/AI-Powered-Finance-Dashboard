"""FastAPI application for the crypto market dashboard."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, market
from app.api.core.config import settings

app = FastAPI(
    title="Crypto Dashboard API",
    description="Authentication, market candles, and market analytics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(market.router)
app.include_router(analytics.router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness check; deliberately does not require a database connection."""
    return {"status": "ok"}
