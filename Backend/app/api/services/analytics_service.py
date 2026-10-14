"""Daily return analytics computed from ordered candle rows."""

from collections import defaultdict
from math import sqrt


def daily_closes(rows: list[dict]) -> dict[str, list[tuple[str, float]]]:
    closes: dict[str, dict[str, float]] = defaultdict(dict)
    for row in rows:
        date = row["open_time"].date().isoformat()
        closes[row["ticker"]][date] = float(row["close"])
    return {
        ticker: sorted(days.items())
        for ticker, days in sorted(closes.items())
    }


def pct_change(rows: list[dict]) -> list[dict]:
    by_ticker = daily_closes(rows)
    if not by_ticker:
        return []
    date_sets = [set(dict(points)) for points in by_ticker.values()]
    common_dates = sorted(set.intersection(*date_sets))
    if not common_dates:
        return []
    bases = {ticker: dict(points)[common_dates[0]] for ticker, points in by_ticker.items()}
    return [
        {
            "date": date,
            "values": {
                ticker: round((dict(points)[date] / bases[ticker] - 1) * 100, 2)
                for ticker, points in by_ticker.items()
            },
        }
        for date in common_dates
    ]


def volatility(rows: list[dict], ticker: str, window: int = 7) -> list[dict]:
    points = daily_closes(rows).get(ticker, [])
    returns = []
    return_dates = []
    for index in range(1, len(points)):
        if points[index - 1][1] != 0:
            returns.append(points[index][1] / points[index - 1][1] - 1)
            return_dates.append(points[index][0])
    result = []
    for index in range(window, len(returns) + 1):
        sample = returns[index - window:index]
        mean = sum(sample) / window
        variance = sum((value - mean) ** 2 for value in sample) / window
        result.append({"date": return_dates[index - 1], "volatility": round(sqrt(variance) * 100, 2)})
    return result


def correlation(rows: list[dict]) -> dict:
    by_ticker = daily_closes(rows)
    tickers = list(by_ticker)
    returns: dict[str, dict[str, float]] = {}
    for ticker, points in by_ticker.items():
        ticker_returns = {}
        for index in range(1, len(points)):
            if points[index - 1][1] != 0:
                ticker_returns[points[index][0]] = (
                    points[index][1] / points[index - 1][1] - 1
                )
        returns[ticker] = ticker_returns

    def pearson(left: str, right: str) -> float:
        dates = sorted(set(returns[left]) & set(returns[right]))
        if len(dates) < 2:
            return 0.0
        x = [returns[left][date] for date in dates]
        y = [returns[right][date] for date in dates]
        mean_x, mean_y = sum(x) / len(x), sum(y) / len(y)
        covariance = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
        variance_x = sum((a - mean_x) ** 2 for a in x)
        variance_y = sum((b - mean_y) ** 2 for b in y)
        denominator = sqrt(variance_x * variance_y)
        return round(covariance / denominator, 2) if denominator else 0.0

    return {"tickers": tickers, "values": [[pearson(a, b) for b in tickers] for a in tickers]}
