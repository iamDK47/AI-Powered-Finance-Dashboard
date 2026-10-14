"""Parameterized SQL queries for market data."""

KLINES_QUERY = """
    SELECT ticker, open_time, open, high, low, close, coin_volume,
           quote_asset_volume, total_trades, market_buy_volume,
           market_buy_quote_volume, delta, close_time
    FROM global_crypto_data
    WHERE ticker = %s
      AND (%s IS NULL OR open_time >= %s)
      AND (%s IS NULL OR open_time <= %s)
    ORDER BY open_time ASC
    LIMIT %s
"""

TICKERS_QUERY = """
    SELECT DISTINCT ticker
    FROM global_crypto_data
    ORDER BY ticker ASC
"""
