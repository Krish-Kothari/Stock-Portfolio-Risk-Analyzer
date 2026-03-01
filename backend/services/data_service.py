"""
Data Service — fetches historical prices from Yahoo Finance, computes returns
and covariance matrices.  Includes a simple session-level cache.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from config import TRADING_DAYS_PER_YEAR, DEFAULT_PERIOD, BENCHMARK_TICKER

# ---------------------------------------------------------------------------
# In-memory price cache  (ticker+period → DataFrame)
# ---------------------------------------------------------------------------
_price_cache = {}  # type: dict


def _cache_key(tickers: list[str], period: str) -> str:
    return f"{','.join(sorted(tickers))}|{period}"


def clear_cache():
    """Clear the in-memory price cache."""
    _price_cache.clear()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch_prices(tickers: list[str], period: str = DEFAULT_PERIOD) -> pd.DataFrame:
    """
    Download adjusted-close prices for *tickers* over *period*.
    Returns a DataFrame indexed by date with one column per ticker.
    Raises ValueError if any ticker has no data.
    """
    key = _cache_key(tickers, period)
    if key in _price_cache:
        return _price_cache[key]

    all_tickers = list(set(tickers))  # deduplicate
    data = yf.download(all_tickers, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError(f"No price data returned for tickers: {all_tickers}")

    # yf.download returns MultiIndex columns when >1 ticker
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = all_tickers

    # Check for tickers that returned no data
    missing = [t for t in all_tickers if t not in prices.columns or prices[t].isna().all()]
    if missing:
        raise ValueError(f"No data found for ticker(s): {missing}")

    prices = prices.dropna()
    _price_cache[key] = prices
    return prices


def fetch_prices_with_benchmark(
    tickers: list[str],
    period: str = DEFAULT_PERIOD,
    benchmark: str = BENCHMARK_TICKER,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Fetch prices for *tickers* AND the benchmark index.
    Returns (asset_prices DataFrame, benchmark_prices Series).
    """
    all_tickers = list(set(tickers + [benchmark]))
    prices = fetch_prices(all_tickers, period)
    benchmark_prices = prices[benchmark]
    asset_prices = prices[[t for t in tickers if t in prices.columns]]
    return asset_prices, benchmark_prices


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily simple (percentage) returns."""
    return prices.pct_change().dropna()


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily log returns."""
    return np.log(prices / prices.shift(1)).dropna()


def compute_covariance(returns: pd.DataFrame, annualize: bool = True) -> pd.DataFrame:
    """
    Compute the covariance matrix of daily returns.
    If *annualize* is True, multiply by TRADING_DAYS_PER_YEAR.
    """
    cov = returns.cov()
    if annualize:
        cov *= TRADING_DAYS_PER_YEAR
    return cov


def compute_correlation(returns: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation matrix of daily returns."""
    return returns.corr()


def validate_tickers(tickers: list[str]) -> dict:
    """
    Check which tickers are valid (have data on Yahoo Finance).
    Returns {"valid": [...], "invalid": [...]}.
    """
    valid, invalid = [], []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker)
            hist = info.history(period="5d")
            if hist.empty:
                invalid.append(ticker)
            else:
                valid.append(ticker)
        except Exception:
            invalid.append(ticker)
    return {"valid": valid, "invalid": invalid}


def get_portfolio_returns(
    holdings: list[dict],
    period: str = DEFAULT_PERIOD,
) -> tuple[pd.Series, pd.DataFrame]:
    """
    Compute weighted portfolio daily returns from a holdings list.
    Each holding: {"ticker": "AAPL", "weight": 0.4}
    Returns (portfolio_returns Series, individual_returns DataFrame).
    """
    tickers = [h["ticker"] for h in holdings]
    weights = np.array([h["weight"] for h in holdings])

    prices = fetch_prices(tickers, period)
    returns = compute_returns(prices)

    # Align columns order with tickers
    returns = returns[tickers]
    portfolio_returns = returns.dot(weights)
    return portfolio_returns, returns


def fetch_live_prices(tickers: list[str]) -> list[dict]:
    """
    Fetch current live price and daily change for a list of tickers.
    Returns a list of dicts: {"ticker": str, "price": float, "change": float, "change_pct": float}
    """
    results = []
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="5d")
            if len(hist) >= 2:
                current_price = float(hist["Close"].iloc[-1])
                prev_close = float(hist["Close"].iloc[-2])
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                results.append({
                    "ticker": ticker,
                    "price": round(current_price, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2)
                })
        except Exception:
            pass
    return results
