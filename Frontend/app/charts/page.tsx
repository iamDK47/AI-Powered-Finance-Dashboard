"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../AuthProvider";
import { CorrelationHeatmap } from "../../CorrelationHeatmap";
import { PctChangeLines } from "../../PctChangeLines";
import { VolatilityChart } from "../../VolatilityChart";
import { getCorrelation, getPerformance, getTickers, getVolatility } from "../../api";
import { generateMockCorrelationMatrix, generateMockPctChangeSeries, generateMockVolatilitySeries } from "../../mockData";
import { CorrelationMatrix, PctChangePoint, VolatilityPoint } from "../../types";

const DEMO_TICKERS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"];

export default function ChartsPage() {
  const { user, isGuest, isLoading, logout } = useAuth();
  const router = useRouter();
  const [tickers, setTickers] = useState(DEMO_TICKERS);
  const [selected, setSelected] = useState("BTCUSDT");
  const [performance, setPerformance] = useState<PctChangePoint[]>([]);
  const [volatility, setVolatility] = useState<VolatilityPoint[]>([]);
  const [correlation, setCorrelation] = useState<CorrelationMatrix>({ tickers: [], values: [] });
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isLoading) return;
    if (!user && !isGuest) { router.replace("/login"); return; }
    let cancelled = false;
    async function load() {
      setBusy(true); setError("");
      if (isGuest) {
        setTickers(DEMO_TICKERS); setPerformance(generateMockPctChangeSeries(DEMO_TICKERS));
        setVolatility(generateMockVolatilitySeries()); setCorrelation(generateMockCorrelationMatrix(DEMO_TICKERS));
        setBusy(false); return;
      }
      try {
        const token = user!.token;
        const [symbols, rawPerformance, matrix] = await Promise.all([getTickers(token), getPerformance(token), getCorrelation(token)]);
        if (cancelled) return;
        const available = symbols.slice(0, 8);
        setTickers(available); setSelected(current => available.includes(current) ? current : (available[0] ?? ""));
        setPerformance(rawPerformance.map(point => ({ date: point.date, ...point.values })));
        setCorrelation(matrix);
        if (available[0]) {
          const vol = await getVolatility(token, available[0]);
          if (!cancelled) setVolatility(vol);
        }
      } catch (e) {
        if (!cancelled) {
          if (e instanceof Error && e.message === "UNAUTHORIZED") { logout(); router.replace("/login"); return; }
          setError(e instanceof Error ? `${e.message}. Check that the API and PostgreSQL database are running.` : "Could not load dashboard data.");
        }
      } finally { if (!cancelled) setBusy(false); }
    }
    void load();
    return () => { cancelled = true; };
  }, [isLoading, user, isGuest, logout, router]);

  useEffect(() => {
    if (!user || isGuest || !selected) return;
    let cancelled = false;
    getVolatility(user.token, selected).then(value => { if (!cancelled) setVolatility(value); }).catch(e => {
      if (!cancelled && e instanceof Error && e.message === "UNAUTHORIZED") { logout(); router.replace("/login"); }
    });
    return () => { cancelled = true; };
  }, [selected, user, isGuest, logout, router]);

  if (isLoading || busy) return <div className="mx-auto max-w-6xl px-4 py-16 text-muted">Loading dashboard…</div>;
  return <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="text-sm font-medium uppercase tracking-widest text-accent">Market overview</p><h1 className="mt-2 text-3xl font-semibold">Charts</h1><p className="mt-2 text-sm text-muted">{isGuest ? "Demo mode · generated sample data" : "Connected to your FastAPI market data"}</p></div>
      {tickers.length > 0 && <label className="text-sm text-muted">Volatility ticker<select value={selected} onChange={e => setSelected(e.target.value)} className="ml-2 rounded-md border border-line bg-surface px-3 py-2 text-foreground">{tickers.map(t => <option key={t}>{t}</option>)}</select></label>}
    </div>
    {error && <div role="alert" className="mt-6 rounded-lg border border-negative/40 bg-negative/10 p-4 text-sm text-negative">{error} <Link className="underline" href="/login">Sign in again</Link></div>}
    <div className="mt-8 grid gap-5">
      <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Relative performance</h2><p className="mt-1 text-xs text-muted">Daily percent change from the first available date.</p></div>{performance.length ? <PctChangeLines data={performance} tickers={tickers} /> : <p className="py-16 text-center text-sm text-muted">No performance data available yet.</p>}</section>
      <div className="grid gap-5 lg:grid-cols-2">
        <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Rolling volatility · {selected || "—"}</h2><p className="mt-1 text-xs text-muted">Seven day standard deviation of daily returns.</p></div>{volatility.length ? <VolatilityChart data={volatility} /> : <p className="py-16 text-center text-sm text-muted">No volatility data available.</p>}</section>
        <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Return correlation</h2><p className="mt-1 text-xs text-muted">Pearson correlation; values range from −1 to 1.</p></div>{correlation.tickers.length ? <CorrelationHeatmap matrix={correlation} /> : <p className="py-16 text-center text-sm text-muted">No correlation data available.</p>}</section>
      </div>
    </div>
  </div>;
}
