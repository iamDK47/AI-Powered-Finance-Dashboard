// Central type definitions. Import these anywhere instead of re-declaring
// shapes locally — one source of truth means a backend field rename only
// needs to be fixed in ONE place (here) instead of hunting through every
// component that touches Kline data.

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

// A point on the normalized "% change since start" line chart.
export interface PctChangePoint {
  date: string;
  [ticker: string]: number | string; // one numeric key per asset, e.g. BTCUSDT: 4.2
}

export interface VolatilityPoint {
  date: string;
  volatility: number;
}

// Correlation matrix: square grid, tickers on both axes.
export interface CorrelationMatrix {
  tickers: string[];
  values: number[][]; // values[i][j] = correlation between tickers[i] and tickers[j], range -1 to 1
}
