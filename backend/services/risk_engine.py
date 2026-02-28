"""
Risk Engine — computes portfolio-level financial risk metrics.

Metrics implemented:
  • Historical VaR / CVaR
  • Parametric (Gaussian) VaR / CVaR
  • Sharpe Ratio
  • Sortino Ratio
  • Beta & Alpha (vs. benchmark)
  • Maximum Drawdown
  • Annualized Volatility
"""

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

from config import (
    RISK_FREE_RATE,
    TRADING_DAYS_PER_YEAR,
    DEFAULT_CONFIDENCE_LEVEL,
    BENCHMARK_TICKER,
    DEFAULT_PERIOD,
)
from services.data_service import (
    fetch_prices_with_benchmark,
    compute_returns,
    compute_correlation,
    compute_covariance,
    get_portfolio_returns,
    fetch_prices,
)


# -------------------------------------------------------------------------
# Value at Risk
# -------------------------------------------------------------------------

def historical_var(
    returns: pd.Series,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Historical VaR at *confidence* level.
    Returns a positive number representing the loss threshold.
    """
    return float(-np.percentile(returns, (1 - confidence) * 100))


def parametric_var(
    returns: pd.Series,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Parametric (variance-covariance) VaR assuming normal distribution.
    """
    mu = returns.mean()
    sigma = returns.std()
    z = sp_stats.norm.ppf(1 - confidence)
    return float(-(mu + z * sigma))


def historical_cvar(
    returns: pd.Series,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Conditional VaR (Expected Shortfall) — mean of losses beyond VaR.
    """
    var = -historical_var(returns, confidence)  # make negative (loss)
    return float(-returns[returns <= var].mean())


def parametric_cvar(
    returns: pd.Series,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
) -> float:
    """
    Parametric CVaR assuming normal distribution.
    """
    mu = returns.mean()
    sigma = returns.std()
    z = sp_stats.norm.ppf(1 - confidence)
    es = mu - sigma * sp_stats.norm.pdf(z) / (1 - confidence)
    return float(-es)


# -------------------------------------------------------------------------
# Risk-Adjusted Performance
# -------------------------------------------------------------------------

def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = RISK_FREE_RATE,
) -> float:
    """
    Annualized Sharpe Ratio.
    """
    excess = returns.mean() - risk_free_rate / TRADING_DAYS_PER_YEAR
    annual_excess = excess * TRADING_DAYS_PER_YEAR
    annual_vol = returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    if annual_vol == 0:
        return 0.0
    return float(annual_excess / annual_vol)


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = RISK_FREE_RATE,
) -> float:
    """
    Annualized Sortino Ratio — uses downside deviation only.
    """
    daily_rf = risk_free_rate / TRADING_DAYS_PER_YEAR
    excess = returns.mean() - daily_rf
    downside = returns[returns < 0]
    if len(downside) == 0:
        return float("inf")
    downside_std = downside.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    annual_excess = excess * TRADING_DAYS_PER_YEAR
    if downside_std == 0:
        return 0.0
    return float(annual_excess / downside_std)


# -------------------------------------------------------------------------
# Beta & Alpha
# -------------------------------------------------------------------------

def compute_beta(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Beta = Cov(Rp, Rb) / Var(Rb)
    """
    aligned = pd.concat(
        [portfolio_returns, benchmark_returns], axis=1, join="inner"
    )
    aligned.columns = ["portfolio", "benchmark"]
    cov_matrix = aligned.cov()
    beta = cov_matrix.loc["portfolio", "benchmark"] / cov_matrix.loc["benchmark", "benchmark"]
    return float(beta)


def compute_alpha(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float = RISK_FREE_RATE,
) -> float:
    """
    Jensen's Alpha (annualized).
    α = Rp − [Rf + β × (Rb − Rf)]
    """
    beta = compute_beta(portfolio_returns, benchmark_returns)
    rp = portfolio_returns.mean() * TRADING_DAYS_PER_YEAR
    rb = benchmark_returns.mean() * TRADING_DAYS_PER_YEAR
    alpha = rp - (risk_free_rate + beta * (rb - risk_free_rate))
    return float(alpha)


# -------------------------------------------------------------------------
# Drawdown
# -------------------------------------------------------------------------

def max_drawdown(returns: pd.Series) -> float:
    """
    Maximum drawdown from the cumulative return series.
    Returns a positive number.
    """
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    return float(-drawdown.min())


# -------------------------------------------------------------------------
# Volatility
# -------------------------------------------------------------------------

def annualized_volatility(returns: pd.Series) -> float:
    """Annualized standard deviation of daily returns."""
    return float(returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))


def annualized_return(returns: pd.Series) -> float:
    """Annualized mean return."""
    return float(returns.mean() * TRADING_DAYS_PER_YEAR)


# -------------------------------------------------------------------------
# Aggregate: full risk dashboard
# -------------------------------------------------------------------------

def compute_all_metrics(
    holdings: list[dict],
    period: str = DEFAULT_PERIOD,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
    risk_free_rate: float = RISK_FREE_RATE,
    investment_amount: float = 100_000,
) -> dict:
    """
    Compute the full risk dashboard for the given portfolio holdings.
    Returns a dict with all metrics plus metadata.
    """
    tickers = [h["ticker"] for h in holdings]
    weights = np.array([h["weight"] for h in holdings])

    # Fetch data (assets + benchmark)
    asset_prices, benchmark_prices = fetch_prices_with_benchmark(tickers, period)
    asset_returns = compute_returns(asset_prices)
    benchmark_returns = compute_returns(benchmark_prices.to_frame()).iloc[:, 0]

    # Portfolio returns
    asset_returns_aligned = asset_returns[tickers]
    portfolio_returns = asset_returns_aligned.dot(weights)

    # Align portfolio and benchmark
    common_idx = portfolio_returns.index.intersection(benchmark_returns.index)
    port_ret = portfolio_returns.loc[common_idx]
    bench_ret = benchmark_returns.loc[common_idx]

    # --- Compute metrics ---
    hist_var = historical_var(port_ret, confidence)
    param_var = parametric_var(port_ret, confidence)
    hist_cvar = historical_cvar(port_ret, confidence)
    param_cvar = parametric_cvar(port_ret, confidence)
    sharpe = sharpe_ratio(port_ret, risk_free_rate)
    sortino = sortino_ratio(port_ret, risk_free_rate)
    beta = compute_beta(port_ret, bench_ret)
    alpha = compute_alpha(port_ret, bench_ret, risk_free_rate)
    mdd = max_drawdown(port_ret)
    vol = annualized_volatility(port_ret)
    ann_ret = annualized_return(port_ret)

    # Dollar amounts
    daily_var_dollar = hist_var * investment_amount

    return {
        "portfolio_summary": {
            "tickers": tickers,
            "weights": weights.tolist(),
            "period": period,
            "investment_amount": investment_amount,
            "trading_days": len(port_ret),
        },
        "return_metrics": {
            "annualized_return": round(ann_ret, 6),
            "annualized_return_pct": round(ann_ret * 100, 2),
            "total_return": round(float((1 + port_ret).prod() - 1), 6),
            "total_return_pct": round(float((1 + port_ret).prod() - 1) * 100, 2),
        },
        "risk_metrics": {
            "annualized_volatility": round(vol, 6),
            "annualized_volatility_pct": round(vol * 100, 2),
            "max_drawdown": round(mdd, 6),
            "max_drawdown_pct": round(mdd * 100, 2),
        },
        "var_metrics": {
            "confidence_level": confidence,
            "historical_var_1d": round(hist_var, 6),
            "historical_var_1d_pct": round(hist_var * 100, 4),
            "historical_var_1d_dollar": round(daily_var_dollar, 2),
            "parametric_var_1d": round(param_var, 6),
            "parametric_var_1d_pct": round(param_var * 100, 4),
            "historical_cvar_1d": round(hist_cvar, 6),
            "historical_cvar_1d_pct": round(hist_cvar * 100, 4),
            "parametric_cvar_1d": round(param_cvar, 6),
            "parametric_cvar_1d_pct": round(param_cvar * 100, 4),
        },
        "performance_ratios": {
            "sharpe_ratio": round(sharpe, 4),
            "sortino_ratio": round(sortino, 4),
        },
        "benchmark_metrics": {
            "benchmark": BENCHMARK_TICKER,
            "beta": round(beta, 4),
            "alpha": round(alpha, 6),
            "alpha_pct": round(alpha * 100, 2),
        },
        "historical_performance": {
            "dates": port_ret.index.strftime("%Y-%m-%d").tolist(),
            "portfolio": (1 + port_ret).cumprod().round(4).tolist(),
            "benchmark": (1 + bench_ret).cumprod().round(4).tolist(),
        }
    }


def compute_correlation_matrix(
    holdings: list[dict],
    period: str = DEFAULT_PERIOD,
) -> dict:
    """
    Compute the Pearson correlation matrix for all assets in the portfolio.
    Returns a serialisable dict.
    """
    tickers = [h["ticker"] for h in holdings]
    prices = fetch_prices(tickers, period)
    returns = compute_returns(prices)[tickers]
    corr = compute_correlation(returns)
    cov = compute_covariance(returns, annualize=True)

    return {
        "tickers": tickers,
        "correlation_matrix": corr.round(4).values.tolist(),
        "covariance_matrix": cov.round(8).values.tolist(),
    }


def compute_individual_risk(
    holdings: list[dict],
    period: str = DEFAULT_PERIOD,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
    risk_free_rate: float = RISK_FREE_RATE,
) -> list[dict]:
    """
    Per-asset risk breakdown — VaR, Sharpe, volatility for each holding.
    """
    tickers = [h["ticker"] for h in holdings]
    weights_map = {h["ticker"]: h["weight"] for h in holdings}

    asset_prices, benchmark_prices = fetch_prices_with_benchmark(tickers, period)
    asset_returns = compute_returns(asset_prices)
    benchmark_returns = compute_returns(benchmark_prices.to_frame()).iloc[:, 0]

    results = []
    for ticker in tickers:
        ret = asset_returns[ticker]
        common_idx = ret.index.intersection(benchmark_returns.index)

        results.append({
            "ticker": ticker,
            "weight": weights_map[ticker],
            "annualized_return_pct": round(annualized_return(ret) * 100, 2),
            "annualized_volatility_pct": round(annualized_volatility(ret) * 100, 2),
            "historical_var_1d_pct": round(historical_var(ret, confidence) * 100, 4),
            "sharpe_ratio": round(sharpe_ratio(ret, risk_free_rate), 4),
            "beta": round(compute_beta(ret.loc[common_idx], benchmark_returns.loc[common_idx]), 4),
            "max_drawdown_pct": round(max_drawdown(ret) * 100, 2),
        })

    return results
