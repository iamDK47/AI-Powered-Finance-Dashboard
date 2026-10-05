from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, klines

app = FastAPI(title="Crypto Dashboard API")

# CORS exists because browsers block a page on one origin (localhost:3000)
# from calling an API on a different origin (localhost:8000) UNLESS that
# API explicitly says it's allowed to. This middleware is your API saying
# "these origins may call me." Note: allow_origins is an exact allow-list,
# NEVER "*" — and "*" combined with allow_credentials=True isn't just bad
# practice, browsers reject that combination outright.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(klines.router)


@app.get("/health")
def health():
    return {"status": "ok"}
