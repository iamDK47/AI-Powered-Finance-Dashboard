// DEMO DATA ONLY. Every function here generates plausible-looking but fake
// numbers — used for guest mode (so someone without an account still sees a
// working dashboard) and so you can run `npm run dev` and see real-looking
// charts before your FastAPI backend is wired up.
//
// Nothing in this file should still be imported once real API calls are
// live for logged-in users — see app/charts/page.tsx for where the
// guest/logged-in branch happens.

import { PctChangePoint, VolatilityPoint, CorrelationMatrix } from "./types";

function seededRandom(seed: number) {
  // Deterministic pseudo-random so the demo looks the same on every
  // reload instead of jumping around — makes screenshots/demos consistent.
  let s = seed;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

export function generateMockPctChangeSeries(
  tickers: string[],
  days: number = 30
): PctChangePoint[] {
  const rand = seededRandom(42);
  const cumulative: Record<string, number> = {};
  tickers.forEach((t) => (cumulative[t] = 0));

  const points: PctChangePoint[] = [];
  const today = new Date();

  for (let i = days; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const point: PctChangePoint = { date: date.toISOString().slice(0, 10) };

    tickers.forEach((ticker) => {
      const step = (rand() - 0.48) * 4; // slight upward drift, like a real market most days
      cumulative[ticker] += step;
      point[ticker] = Math.round(cumulative[ticker] * 100) / 100;
    });

    points.push(point);
  }

  return points;
}

export function generateMockVolatilitySeries(days: number = 30): VolatilityPoint[] {
  const rand = seededRandom(7);
  const points: VolatilityPoint[] = [];
  const today = new Date();
  let level = 2.5;

  for (let i = days; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    level = Math.max(0.5, level + (rand() - 0.5) * 0.8);
    points.push({ date: date.toISOString().slice(0, 10), volatility: Math.round(level * 100) / 100 });
  }

  return points;
}

export function generateMockCorrelationMatrix(tickers: string[]): CorrelationMatrix {
  const rand = seededRandom(99);
  const n = tickers.length;
  const values: number[][] = Array.from({ length: n }, () => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    for (let j = i; j < n; j++) {
      if (i === j) {
        values[i][j] = 1;
      } else {
        const corr = Math.round((rand() * 1.6 - 0.3) * 100) / 100;
        const clamped = Math.max(-1, Math.min(1, corr));
        values[i][j] = clamped;
        values[j][i] = clamped; // correlation matrices are symmetric
      }
    }
  }

  return { tickers, values };
}
