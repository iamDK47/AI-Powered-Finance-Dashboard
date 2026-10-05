import { Kline, LoginResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function login(username: string, password: string): Promise<LoginResponse> {
  // The FastAPI backend's /auth/login uses OAuth2PasswordRequestForm, which
  // expects form-encoded data, not JSON — sending JSON.stringify here would
  // get a 422 with no obvious reason why. See the backend README for the
  // full explanation; this is the one detail that bites people every time.
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);

  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    throw new Error(res.status === 401 ? "Incorrect username or password" : `Login failed (${res.status})`);
  }
  return res.json();
}

export async function getKlines(
  token: string,
  params: { ticker: string; start?: string; end?: string; limit?: number }
): Promise<Kline[]> {
  const query = new URLSearchParams({ ticker: params.ticker });
  if (params.start) query.set("start", params.start);
  if (params.end) query.set("end", params.end);
  if (params.limit) query.set("limit", String(params.limit));

  const res = await fetch(`${API_BASE_URL}/klines?${query}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 401) {
    // Token expired or invalid — the caller (AuthProvider) is responsible
    // for reacting to this, e.g. logging the user out. This function's
    // only job is to surface it clearly, not to decide what happens next.
    throw new Error("UNAUTHORIZED");
  }
  if (!res.ok) {
    throw new Error(`Failed to fetch klines (${res.status})`);
  }
  return res.json();
}
