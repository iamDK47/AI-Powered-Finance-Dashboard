# FastAPI backend

This public, read-only API powers the OrderFlow dashboard. FastAPI validates requests and responses; PostgreSQL supplies market candles; the service layer queries data and computes analytics.

## Endpoints

- `GET /health` confirms the API process is responding; it does not check PostgreSQL.
- `GET /tickers` returns symbols in `global_crypto_data`.
- `GET /klines?ticker=BTCUSDT&limit=1000` returns oldest-first candle rows.
- `GET /analytics/performance` returns daily percentage changes by ticker.
- `GET /analytics/volatility?ticker=BTCUSDT&window=7` returns rolling daily-return volatility.
- `GET /analytics/correlation` returns a Pearson correlation matrix.

All market and analytics endpoints are public and read-only. Anyone who can reach the API can call them directly. CORS is not authentication or rate limiting. OpenAPI documentation is available at `/docs`.

## Run locally

Open PowerShell in this `Backend` directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in `Backend` (the settings loader reads `.env` from the process working directory):

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_dashboard
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_SSLMODE=prefer
CORS_ORIGINS=["http://localhost:3000"]
```

Do not commit database credentials. Start the API from `Backend`:

```powershell
uvicorn app.main:app --reload --port 8000
```

The API can start without PostgreSQL because its connection pool is lazy; data routes return HTTP 503 if PostgreSQL is unavailable.

## Database

The API does not create or populate tables. Create the `crypto_dashboard` database and a `global_crypto_data` table with the expected columns:

| Column | Expected meaning/type |
|---|---|
| `ticker` | Symbol text, e.g. `BTCUSDT` |
| `open_time`, `close_time` | Timestamp or timestamptz |
| `open`, `high`, `low`, `close` | Numeric prices |
| `coin_volume`, `quote_asset_volume` | Numeric volumes |
| `total_trades` | Integer trade count |
| `market_buy_volume`, `market_buy_quote_volume`, `delta` | Numeric market statistics |

These column names must agree with the ingestion pipeline. SQL values are parameterized.

## Request flow

1. `app/main.py` creates the FastAPI app, configures CORS, and registers routers.
2. FastAPI matches the HTTP method and path, then validates query parameters.
3. `Depends(get_db)` supplies a pooled PostgreSQL connection.
4. Route functions call database or analytics services.
5. Pydantic response schemas validate the result; FastAPI serializes it as JSON.

## Deployment

Deploy the API and PostgreSQL database on a host that supports Python and PostgreSQL connectivity. Configure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` as backend environment variables. Set `DB_SSLMODE=require` when the hosted database requires TLS. Set `CORS_ORIGINS` to the frontend's exact public HTTPS origin, and configure the frontend's `NEXT_PUBLIC_API_URL` to the API's public HTTPS URL. Load and verify the market data before expecting charts to show real values.

Because data routes are public, apply hosting-level or application-level rate limits and monitor database load before promoting the app broadly. Do not put database credentials in frontend environment variables.
