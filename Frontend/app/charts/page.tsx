"use client";

import { useEffect, useState } from "react";
import { CorrelationHeatmap } from "../../CorrelationHeatmap";
import { PctChangeLines } from "../../PctChangeLines";
import { VolatilityChart } from "../../VolatilityChart";
import { getCorrelation, getPerformance, getTickers, getVolatility } from "../../api";
import { CorrelationMatrix, PctChangePoint, VolatilityPoint } from "../../types";

export default function ChartsPage() {
  const [tickers, setTickers] = useState<string[]>([]);
  const [selected, setSelected] = useState("");
  const [performance, setPerformance] = useState<PctChangePoint[]>([]);
  const [volatility, setVolatility] = useState<VolatilityPoint[]>([]);
  const [correlation, setCorrelation] = useState<CorrelationMatrix>({ tickers: [], values: [] });
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [symbols, rawPerformance, matrix] = await Promise.all([
          getTickers(),
          getPerformance(),
          getCorrelation(),
        ]);
        if (cancelled) return;
        const available = symbols.slice(0, 8);
        setTickers(available);
        setSelected(current => available.includes(current) ? current : (available[0] ?? ""));
        setPerformance(rawPerformance.map(point => ({ date: point.date, ...point.values })));
        setCorrelation(matrix);
      } catch {
        if (!cancelled) setError("Could not load dashboard data. Check that the API and database are available.");
      } finally {
        if (!cancelled) setBusy(false);
      }
    }
    void load();
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (busy || !selected) return;
    let cancelled = false;
    getVolatility(selected).then(value => {
      if (!cancelled) setVolatility(value);
    }).catch(() => {
      if (!cancelled) setError("Could not load volatility data.");
    });
    return () => { cancelled = true; };
  }, [busy, selected]);

  if (busy) return <div className="mx-auto max-w-6xl px-4 py-16 text-muted">Loading dashboard…</div>;
  return <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div><p className="text-sm font-medium uppercase tracking-widest text-accent">Market overview</p><h1 className="mt-2 text-3xl font-semibold">Charts</h1><p className="mt-2 text-sm text-muted">Live data from the market API</p></div>
      {tickers.length > 0 && <label className="text-sm text-muted">Volatility ticker<select value={selected} onChange={e => setSelected(e.target.value)} className="ml-2 rounded-md border border-line bg-surface px-3 py-2 text-foreground">{tickers.map(t => <option key={t}>{t}</option>)}</select></label>}
    </div>
    {error && <div role="alert" className="mt-6 rounded-lg border border-negative/40 bg-negative/10 p-4 text-sm text-negative">{error}</div>}
    <div className="mt-8 grid gap-5">
      <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Relative performance</h2><p className="mt-1 text-xs text-muted">Daily percent change from the first available date.</p></div>{performance.length ? <PctChangeLines data={performance} tickers={tickers} /> : <p className="py-16 text-center text-sm text-muted">No performance data available yet.</p>}</section>
      <div className="grid gap-5 lg:grid-cols-2">
        <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Rolling volatility · {selected || "—"}</h2><p className="mt-1 text-xs text-muted">Seven day standard deviation of daily returns.</p></div>{volatility.length ? <VolatilityChart data={volatility} /> : <p className="py-16 text-center text-sm text-muted">No volatility data available.</p>}</section>
        <section className="rounded-xl border border-line bg-surface p-5"><div className="mb-4"><h2 className="font-semibold">Return correlation</h2><p className="mt-1 text-xs text-muted">Pearson correlation; values range from −1 to 1.</p></div>{correlation.tickers.length ? <CorrelationHeatmap matrix={correlation} /> : <p className="py-16 text-center text-sm text-muted">No correlation data available.</p>}</section>
      </div>
    </div>
  </div>;
}
