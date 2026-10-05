# Crypto Dashboard API

Tested and passing: health check works independent of the database, login
issues real JWTs, protected routes correctly reject missing/invalid tokens
BEFORE touching the database, and a database outage returns a clean 503
instead of crashing the app.

## Setup (do this first)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

1. `cp .env.example .env`
2. Fill in your real Postgres credentials in `.env`.
3. Generate your admin password hash:
   ```bash
   python generate_password_hash.py
   ```
   Paste the printed hash into `ADMIN_PASSWORD_HASH` in `.env`. Pick your own
   `ADMIN_USERNAME`. Generate a random `JWT_SECRET_KEY` too — anything long
   and random works, e.g. `python -c "import secrets; print(secrets.token_hex(32))"`.

## Run it

```bash
uvicorn app.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` — FastAPI auto-generates interactive docs
for every route from the type hints and Pydantic schemas in this codebase.
Click "Authorize," log in with your admin credentials, and you can try every
endpoint from that page before writing any frontend code at all.

## Table assumed

`GET /klines` queries a table named `global_crypto_data` with columns
matching your existing `load_kline` insert: `ticker, open_time, open, high,
low, close, coin_volume, quote_asset_volume, total_trades,
market_buy_volume, market_buy_quote_volume, delta, close_time`. If your real
table or column names differ, update the query in `app/routers/klines.py`
and the field names in `app/schemas.py::KlineOut` to match.

## Connecting the Next.js frontend

1. Copy `frontend-client/lib/api.ts` into your Next.js project.
2. Copy `.env.local.example` to `.env.local` in the Next.js project root.
3. `NEXT_PUBLIC_` prefix is required for any env var Next.js exposes to
   browser-side code — without it, `process.env.NEXT_PUBLIC_API_URL` would
   be `undefined` in the browser (server-only env vars skip the prefix, but
   this one needs to reach client components making the fetch calls).
4. If your Next.js dev server runs on a different port than 3000, update
   `cors_origins` in `app/config.py` to match.

## Token storage — a real tradeoff, not a solved problem

The example in `api.ts` keeps the JWT in React state, which disappears on
refresh — fine for testing tomorrow. Two real options once this matters:

- **localStorage** — simplest to wire up, but readable by any JS that runs
  on your page, so an XSS vulnerability anywhere in your frontend means
  token theft. Common in practice, not the most secure option.
- **httpOnly cookie** — the browser sends it automatically, and page
  JavaScript can't read it, so it's immune to that specific XSS-theft path.
  Requires the backend to set the cookie on login instead of returning the
  token in the response body, and the frontend to send
  `credentials: "include"` on fetch calls. More correct, more moving parts.

For a solo project, localStorage is a reasonable shortcut. Know the
httpOnly version exists as the answer if this stack is ever asked about in
an interview.

## Growing past single-admin auth

When you actually have more than one user: add a `users` table (id,
username, hashed_password, created_at), replace the hardcoded
`settings.admin_username` / `admin_password_hash` check in
`app/routers/auth.py` with a database lookup by username, and everything
else — JWT creation, `get_current_user`, every protected route — stays
exactly the same. The auth *mechanism* doesn't change, only where the
credential check gets its answer from.

## Production-standard note

This uses a fixed-size connection pool and hand-rolled JWT logic, which is
genuinely fine at this scale. If this ever needs to handle real concurrent
production traffic, the standard next step is `SQLAlchemy` with an async
driver (`asyncpg`) for the database layer, and a library like `fastapi-users`
for auth instead of hand-rolled routes — worth knowing exists, not worth
adopting for a one-person dashboard.
