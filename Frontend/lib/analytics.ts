// Turns raw 1-minute Kline rows (what the backend's /klines endpoint
// actually returns) into the daily-level series the charts need.
//
// The signed-in dashboard calls FastAPI's /analytics endpoints directly.
// These helpers remain available for experiments with raw candle rows.

import { Kline, PctChangePoint, VolatilityPoint, CorrelationMatrix } from "@/types";

interface DailyPoint {
  date: string;
  close: number;
}

export function aggregateToDaily(klines: Kline[]): DailyPoint[] {
  const byDate = new Map<string, number>();
  // Klines are assumed ordered oldest-to-newest (what /klines returns) —
  // each later close for the same day overwrites the earlier one, so
  // byDate ends up holding each day's LAST close, which is what "daily
  // close" means.
  for (const k of klines) {
    const date = k.open_time.slice(0, 10);
    byDate.set(date, k.close);
  }
  return Array.from(byDate.entries()).map(([date, close]) => ({ date, close }));
}

function dailyReturns(daily: DailyPoint[]): number[] {
  const returns: number[] = [];
  for (let i = 1; i < daily.length; i++) {
    returns.push((daily[i].close - daily[i - 1].close) / daily[i - 1].close);
  }
  return returns;
}

export function computePctChangeSeries(
  dailyByTicker: Record<string, DailyPoint[]>
): PctChangePoint[] {
  const tickers = Object.keys(dailyByTicker);
  if (tickers.length === 0) return [];

  const dates = dailyByTicker[tickers[0]].map((d) => d.date);
  const baseClose: Record<string, number> = {};
  tickers.forEach((t) => {
    baseClose[t] = dailyByTicker[t][0]?.close ?? 1;
  });

  return dates.map((date, i) => {
    const point: PctChangePoint = { date };
    tickers.forEach((t) => {
      const close = dailyByTicker[t][i]?.close;
      point[t] = close !== undefined
        ? Math.round(((close - baseClose[t]) / baseClose[t]) * 10000) / 100
        : 0;
    });
    return point;
  });
}

export function computeVolatilitySeries(daily: DailyPoint[], window: number = 7): VolatilityPoint[] {
  const returns = dailyReturns(daily);
  const points: VolatilityPoint[] = [];

  for (let i = window; i <= returns.length; i++) {
    const slice = returns.slice(i - window, i);
    const mean = slice.reduce((a, b) => a + b, 0) / slice.length;
    const variance = slice.reduce((a, b) => a + (b - mean) ** 2, 0) / slice.length;
    const stdDev = Math.sqrt(variance);
    points.push({
      date: daily[i].date,
      volatility: Math.round(stdDev * 10000) / 100, // as a percentage
    });
  }

  return points;
}

export function computeCorrelationMatrix(
  dailyByTicker: Record<string, DailyPoint[]>
): CorrelationMatrix {
  const tickers = Object.keys(dailyByTicker);
  const returnsByTicker = tickers.map((t) => dailyReturns(dailyByTicker[t]));

  function pearson(x: number[], y: number[]): number {
    const n = Math.min(x.length, y.length);
    const meanX = x.slice(0, n).reduce((a, b) => a + b, 0) / n;
    const meanY = y.slice(0, n).reduce((a, b) => a + b, 0) / n;
    let cov = 0, varX = 0, varY = 0;
    for (let i = 0; i < n; i++) {
      const dx = x[i] - meanX;
      const dy = y[i] - meanY;
      cov += dx * dy;
      varX += dx * dx;
      varY += dy * dy;
    }
    if (varX === 0 || varY === 0) return 0;
    return cov / Math.sqrt(varX * varY);
  }

  const values = tickers.map((_, i) =>
    tickers.map((_, j) => Math.round(pearson(returnsByTicker[i], returnsByTicker[j]) * 100) / 100)
  );

  return { tickers, values };
}
