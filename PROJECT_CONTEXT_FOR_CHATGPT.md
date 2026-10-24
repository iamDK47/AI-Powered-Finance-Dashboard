# Project context handoff

Use this as background when helping me with my project. I am learning backend engineering and want explanations that are clear, concrete, and beginner-friendly. Avoid unexplained jargon, distinguish what the framework does from what Python does, and use examples from this codebase. I may ask you to edit code; make only the requested changes and explain them plainly.

## Project overview

This is an AI-powered crypto/finance dashboard with a Next.js/TypeScript frontend, a FastAPI backend, a PostgreSQL database, and a separate Python data pipeline that collects/transforms market data. The backend serves market candles and analytics such as percent change, volatility, and correlation.

Relevant directories:

- `Backend/app/main.py`: creates the FastAPI app, configures CORS, and includes the market and analytics routers.
- `Backend/app/api/routes/`: HTTP endpoints (`market.py`, `analytics.py`).
- `Backend/app/api/services/`: database operations and analytics calculations.
- `Backend/app/api/schemas/`: Pydantic models used for API response shapes.
- `Backend/app/api/database/`: PostgreSQL pool/dependency (`connection.py`) and SQL strings (`queries.py`).
- `Backend/app/api/core/config.py`: environment-backed settings using Pydantic Settings.
- `Pipeline/`: separate Python market-data collection and database code.
- `Frontend/`: Next.js/TypeScript user interface.

## Current backend request flow

1. `Backend/app/main.py` creates `FastAPI()` and calls `app.include_router(market.router)` and `app.include_router(analytics.router)`.
2. Each route module creates `router = APIRouter(...)` and registers functions with decorators such as `@router.get(...)`.
3. FastAPI matches an incoming HTTP request to a route function. It parses/validates route parameters based on the function signature and runs dependencies such as `Depends(get_db)`.
4. The route calls service functions, which use parameterized SQL and the provided database connection.
5. FastAPI applies the declared `response_model`, such as `list[KlineOut]`, to validate/serialize the response.
6. The connection dependency yields a pooled connection to the route and returns it to the pool in `finally` after the request completes.

## Important explanation: annotations vs runtime validation

Please explain these distinctions precisely:

- A Python annotation such as `ticker: str` is normally just metadata/hint. Python does not automatically reject a wrong value when an ordinary function is called.
- FastAPI reads annotations on registered route functions. It parses and validates incoming HTTP parameters before calling the route. For example, it parses a query parameter annotated `limit: int` into an integer and rejects values it cannot parse. This is generally coercive validation, not Pydantic strict mode.
- `Query(...)` can add request constraints, such as required values and minimum/maximum bounds.
- Pydantic validates when a `BaseModel` is constructed or applied as a FastAPI response model. In this backend, `KlineOut`, `TickerList`, and the analytics schemas define response shapes. The market route declares `response_model=list[KlineOut]` and `response_model=TickerList`.
- `Settings(BaseSettings)` is validated/loaded by Pydantic Settings when `settings = Settings()` runs. `model_config` configures that loading (such as `.env` settings).
- Type annotations inside regular service/helper functions, such as `fetch_klines(..., ticker: str, ...)`, `analytics_service.py` functions, and most annotations in `connection.py`, do not automatically validate values. They are hints unless a tool/framework explicitly reads them.
- `connection=Depends(get_db)` is FastAPI dependency injection, not a type check.
- “Strict” has a specific meaning: disallowing otherwise-valid coercions. The project does not currently enable strict Pydantic mode on route parameters/schemas by default.

## Current code simplification

`Backend/app/api/routes/market.py` was simplified at my request. The `/klines` signature currently has basic annotations (`ticker: str`, `start: datetime | None`, `end: datetime | None`, `limit: int = 1000`) without the former detailed `Query(...)` constraints. The date-order check remains. Keep explanations grounded in the current code, and don’t imply `ticker: str` checks that the symbol exists or is a valid exchange ticker.

## Database connection concepts

`Backend/app/api/database/connection.py` uses `psycopg2.pool.ThreadedConnectionPool`. `_get_pool()` lazily creates one pool per backend process with a minimum of 1 and maximum of 10 connections. `get_db()` borrows one with `getconn()`, yields it to FastAPI, then returns it with `putconn()` in `finally`. The pool connects using settings from `config.py`. `HTTPException` handling is API-specific; the separate pipeline has its own database connection setup and may not need a pool if it runs one job/connection at a time.

## Deployment preparation discussed

The project was prepared for a possible free-tier setup using Vercel for the frontend, Render for FastAPI, and Neon for PostgreSQL. Deployment was not actually performed. It requires provider accounts, a Git-hosted repository, hosted database setup/data import, environment variables, and frontend dependency/build verification. `render.yaml` and `DEPLOYMENT.md` were added in that preparation. Verify current provider limits before relying on them because free-tier terms can change.

Login/authentication was removed at the user's request to make the read-only dashboard public. The API endpoints therefore do not require user login. Do not reintroduce auth unless asked.

## Pipeline caution

`Pipeline/stats.py` previously contained a top-level call to `edit_pg()`, which truncates `global_crypto_data`. Do not run/import it casually; confirm before executing anything that could clear data.

## Communication preference

The user is a beginner and asks detailed conceptual questions. Explain with the actual file/function, then say what Python itself does and what FastAPI/Pydantic adds. Avoid broad claims like “Pydantic strictly checks all annotations.” Use small end-to-end examples and correct earlier ambiguity directly. Do not make unsolicited code changes when the user asks for an explanation.
