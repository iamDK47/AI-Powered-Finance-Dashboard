import { CorrelationMatrix, Kline, PctChangePoint, VolatilityPoint } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json() as Promise<T>;
}

export function getKlines(
  params: { ticker: string; start?: string; end?: string; limit?: number }
): Promise<Kline[]> {
  const query = new URLSearchParams({ ticker: params.ticker });
  if (params.start) query.set("start", params.start);
  if (params.end) query.set("end", params.end);
  if (params.limit) query.set("limit", String(params.limit));
  return getJson(`/klines?${query}`);
}

export async function getTickers(): Promise<string[]> {
  const result = await getJson<{ tickers: string[] }>("/tickers");
  return result.tickers;
}

export function getPerformance(): Promise<Array<{ date: string; values: Record<string, number> }>> {
  return getJson("/analytics/performance?limit=1000");
}

export function getVolatility(ticker: string): Promise<VolatilityPoint[]> {
  return getJson(`/analytics/volatility?ticker=${encodeURIComponent(ticker)}&window=7&limit=1000`);
}

export function getCorrelation(): Promise<CorrelationMatrix> {
  return getJson("/analytics/correlation?limit=1000");
}
