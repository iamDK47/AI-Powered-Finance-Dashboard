# FastAPI backend

This folder contains the Python API used by the OrderFlow Next.js dashboard. FastAPI receives HTTP requests, validates inputs, calls the Python route functions, and serializes their return values as JSON. PostgreSQL supplies the market candles; environment variables supply database and admin login settings.

## What the backend does

- `GET /health` confirms the API process is running. It does not check PostgreSQL.
- `POST /auth/login` checks one configured admin username and bcrypt password hash, then returns a signed JWT access token.
- `GET /tickers` returns symbols in `global_crypto_data`.
- `GET /klines?ticker=BTCUSDT&limit=1000` returns oldest-first candle rows for one symbol.
- `GET /analytics/performance` returns daily percentage changes by ticker.
- `GET /analytics/volatility?ticker=BTCUSDT&window=7` returns rolling daily-return volatility.
- `GET /analytics/correlation` returns a Pearson correlation matrix.

Every endpoint other than `/health` and `/auth/login` requires `Authorization: Bearer <token>`. OpenAPI documentation is generated from the routes and schemas at [http://localhost:8000/docs](http://localhost:8000/docs).

## Run the API

Open PowerShell in this `Backend` directory:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

Make a `.env` file in the current `Backend` directory. The settings loader reads `.env` relative to the process working directory, so start Uvicorn from `Backend` as shown below.

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_dashboard
DB_USER=postgres
DB_PASSWORD=your-postgres-password
JWT_SECRET_KEY=replace-this-with-a-long-random-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=paste-the-generated-bcrypt-hash
ACCESS_TOKEN_EXPIRE_MINUTES=720
CORS_ORIGINS=["http://localhost:3000"]
```

Generate the password hash interactively (the script asks for a password and prints a bcrypt hash):

```powershell
python generate_password_hash.py
```

Copy the printed hash into `ADMIN_PASSWORD_HASH`. Do not put your plain password, database password, or JWT signing key in Git. Start the server:

```powershell
uvicorn app.main:app --reload --port 8000
```

Check [http://localhost:8000/health](http://localhost:8000/health). A successful response is `{"status":"ok"}`. The API process can start without a live database because the connection pool is lazy; data routes return HTTP 503 if PostgreSQL is unavailable.

## Database setup

The API does not create a database or table. Create the `crypto_dashboard` database and populate a PostgreSQL table named `global_crypto_data` before using data routes. The expected columns are:

| Column | Expected meaning/type |
|---|---|
| `ticker` | Symbol text, for example `BTCUSDT` |
| `open_time`, `close_time` | PostgreSQL timestamp or timestamp with time zone |
| `open`, `high`, `low`, `close` | Numeric prices |
| `coin_volume`, `quote_asset_volume` | Numeric volumes |
| `total_trades` | Integer trade count |
| `market_buy_volume`, `market_buy_quote_volume`, `delta` | Numeric market statistics |

These names are also used by the existing ingestion pipeline. Ensure its table definition and the API's expected columns agree. The API queries are parameterized; user-provided ticker and date values are not concatenated into SQL.

## How a FastAPI request works here

1. `app/main.py` creates the FastAPI application, configures CORS, and registers the route modules.
2. A route such as `app/api/routes/market.py` declares the HTTP method and URL. FastAPI reads query parameters, checks their declared types/ranges, and returns a 422 response for invalid input.
3. `Depends(get_current_user)` checks the bearer JWT for protected routes. `Depends(get_db)` checks out a pooled PostgreSQL connection for a route and returns it to the pool afterward.
4. The route calls a service in `app/api/services/`. Services run database queries or compute analytics.
5. A Pydantic response schema in `app/api/schemas/` validates and shapes the result. FastAPI encodes it as JSON and sets the HTTP response status.

For example, `GET /klines?ticker=BTCUSDT&limit=1000` has query inputs, token and database dependencies, a service call, and a `list[KlineOut]` response. This structure keeps URL/input validation, database work, and response shape understandable as separate pieces.

## How the frontend talks to this API

The Next.js app runs at `http://localhost:3000`; FastAPI runs at `http://localhost:8000`. These are different browser origins, so `CORS_ORIGINS` must contain the exact frontend origin. After changing it, restart FastAPI.

The sign-in screen sends `POST /auth/login` with `Content-Type: application/x-www-form-urlencoded` and the fields `username` and `password`. This matters: the route uses FastAPI's `OAuth2PasswordRequestForm`, so sending JSON would produce a 422 error. On success, the response resembles:

```json
{"access_token":"eyJ...","token_type":"bearer"}
```

The frontend stores that token in browser local storage and sends `Authorization: Bearer eyJ...` on protected requests. FastAPI validates the signature and expiry before accessing the database. Guest mode exists only in the frontend and displays generated demo values; it does not create a backend account or retrieve private data.

## Add an endpoint

For a new feature, generally add a Pydantic response model in `app/api/schemas/`, a service function for database/computation work in `app/api/services/`, and a route in `app/api/routes/`. Register a new router in `app/main.py` if it is a new route module. Declare query parameters with types and constraints, add a response model, and decide whether the route needs `get_current_user`. Then the frontend can call it from `Frontend/api.ts` and render the typed result.
