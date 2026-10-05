const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Kline {
  ticker: string;
  open_time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  coin_volume: number;
  quote_asset_volume: number;
  total_trades: number;
  market_buy_volume: number;
  market_buy_quote_volume: number;
  delta: number;
  close_time: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export async function login(
  username: string,
  password: string
): Promise<LoginResponse> {
  // FastAPI's OAuth2PasswordRequestForm (used on the backend's /auth/login)
  // expects FORM-encoded data, not JSON. Sending JSON.stringify({username,
  // password}) here would get you a 422 with no obvious explanation —
  // this is the single most common place people get stuck on this stack.
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);

  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    throw new Error(`Login failed: ${res.status}`);
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

  if (!res.ok) {
    throw new Error(`Failed to fetch klines: ${res.status}`);
  }
  return res.json();
}

/*
Example usage in a client component:

  "use client";
  import { useEffect, useState } from "react";
  import { login, getKlines, Kline } from "@/lib/api";

  export default function Dashboard() {
    const [data, setData] = useState<Kline[]>([]);

    useEffect(() => {
      (async () => {
        const { access_token } = await login("daniyal", "your-password");
        const klines = await getKlines(access_token, { ticker: "BTCUSDT", limit: 500 });
        setData(klines);
      })();
    }, []);

    return <pre>{JSON.stringify(data.slice(0, 5), null, 2)}</pre>;
  }

  Storing the token in a useState like this only lasts until refresh — fine
  for testing tomorrow morning. See README's "token storage" note for what
  changes before this goes anywhere real.
*/
