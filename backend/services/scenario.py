"""
Scenario Analysis Engine — shock analysis and historical stress tests.
"""

import numpy as np
import pandas as pd

from config import (
    STRESS_SCENARIOS,
    TRADING_DAYS_PER_YEAR,
    DEFAULT_PERIOD,
    DEFAULT_CONFIDENCE_LEVEL,
    RISK_FREE_RATE,
    BENCHMARK_TICKER,
)
from services.data_service import (
    fetch_prices,
    fetch_prices_with_benchmark,
    compute_returns,
    get_portfolio_returns,
)
from services.risk_engine import (
    historical_var,
    annualized_volatility,
    sharpe_ratio,
    compute_beta,
    max_drawdown,
    annualized_return,
)


def shock_analysis(
    holdings: list[dict],
    shocks: dict[str, float],
    period: str = DEFAULT_PERIOD,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
    investment_amount: float = 100_000,
) -> dict:
    """
    Analyse the impact of one or more asset-level shocks.

    *shocks* maps ticker → fractional change, e.g. {"AAPL": -0.20}
    means "what if AAPL drops 20%?"

    Returns before/after comparison of portfolio value and risk metrics.
    """
    tickers = [h["ticker"] for h in holdings]
    weights = np.array([h["weight"] for h in holdings])
    weight_map = {h["ticker"]: h["weight"] for h in holdings}

    # Fetch prices and returns
    asset_prices, benchmark_prices = fetch_prices_with_benchmark(tickers, period)
    asset_returns = compute_returns(asset_prices)[tickers]
    benchmark_returns = compute_returns(benchmark_prices.to_frame()).iloc[:, 0]
    portfolio_returns = asset_returns.dot(weights)

    common_idx = portfolio_returns.index.intersection(benchmark_returns.index)
    port_ret = portfolio_returns.loc[common_idx]
    bench_ret = benchmark_returns.loc[common_idx]

    # --- Before shock ---
    before = {
        "portfolio_value": investment_amount,
        "annualized_return_pct": round(annualized_return(port_ret) * 100, 2),
        "annualized_volatility_pct": round(annualized_volatility(port_ret) * 100, 2),
        "historical_var_1d_pct": round(historical_var(port_ret, confidence) * 100, 4),
        "sharpe_ratio": round(sharpe_ratio(port_ret), 4),
        "beta": round(compute_beta(port_ret, bench_ret), 4),
        "max_drawdown_pct": round(max_drawdown(port_ret) * 100, 2),
    }

    # --- Calculate shock impact ---
    shock_details = []
    total_impact = 0.0

    for ticker, shock_pct in shocks.items():
        w = weight_map.get(ticker, 0)
        dollar_impact = investment_amount * w * shock_pct
        total_impact += dollar_impact
        shock_details.append({
            "ticker": ticker,
            "shock_pct": round(shock_pct * 100, 2),
            "weight": w,
            "dollar_impact": round(dollar_impact, 2),
            "contribution_to_loss_pct": round(w * shock_pct * 100, 4),
        })

    new_value = investment_amount + total_impact

    # --- Stressed returns (shift mean by shock magnitude) ---
    stressed_returns = asset_returns.copy()
    for ticker, shock_pct in shocks.items():
        if ticker in stressed_returns.columns:
            # Distribute the shock evenly across all days as a mean shift
            daily_shock = shock_pct / len(stressed_returns)
            stressed_returns[ticker] = stressed_returns[ticker] + daily_shock

    stressed_portfolio = stressed_returns[tickers].dot(weights)
    stressed_common = stressed_portfolio.index.intersection(bench_ret.index)
    stressed_port = stressed_portfolio.loc[stressed_common]

    after = {
        "portfolio_value": round(new_value, 2),
        "portfolio_change_pct": round((total_impact / investment_amount) * 100, 2),
        "portfolio_change_dollar": round(total_impact, 2),
        "annualized_return_pct": round(annualized_return(stressed_port) * 100, 2),
        "annualized_volatility_pct": round(annualized_volatility(stressed_port) * 100, 2),
        "historical_var_1d_pct": round(historical_var(stressed_port, confidence) * 100, 4),
        "sharpe_ratio": round(sharpe_ratio(stressed_port), 4),
        "max_drawdown_pct": round(max_drawdown(stressed_port) * 100, 2),
    }

    return {
        "shocks_applied": shock_details,
        "before": before,
        "after": after,
    }


def stress_test(
    holdings: list[dict],
    scenario_key: str,
    period: str = DEFAULT_PERIOD,
    confidence: float = DEFAULT_CONFIDENCE_LEVEL,
    investment_amount: float = 100_000,
) -> dict:
    """
    Apply a predefined historical stress scenario to the portfolio.
    Uses the beta of each asset to scale the market-wide shock.
    """
    if scenario_key not in STRESS_SCENARIOS:
        available = list(STRESS_SCENARIOS.keys())
        raise ValueError(
            f"Unknown scenario '{scenario_key}'. Available: {available}"
        )

    scenario = STRESS_SCENARIOS[scenario_key]
    market_drop = scenario["market_drop"]
    sector_mult = scenario.get("sector_multipliers", {})

    tickers = [h["ticker"] for h in holdings]
    weights = np.array([h["weight"] for h in holdings])
    weight_map = {h["ticker"]: h["weight"] for h in holdings}

    # Fetch data for beta calculation
    asset_prices, benchmark_prices = fetch_prices_with_benchmark(tickers, period)
    asset_returns = compute_returns(asset_prices)[tickers]
    benchmark_returns = compute_returns(benchmark_prices.to_frame()).iloc[:, 0]

    # Compute per-asset shocks based on beta
    asset_shocks = {}
    asset_details = []
    for ticker in tickers:
        ret = asset_returns[ticker]
        common_idx = ret.index.intersection(benchmark_returns.index)
        beta = compute_beta(ret.loc[common_idx], benchmark_returns.loc[common_idx])

        # Apply sector multiplier (default 1.0)
        mult = sector_mult.get("default", 1.0)
        estimated_shock = market_drop * beta * mult

        w = weight_map[ticker]
        dollar_impact = investment_amount * w * estimated_shock

        asset_shocks[ticker] = estimated_shock
        asset_details.append({
            "ticker": ticker,
            "weight": w,
            "beta": round(beta, 4),
            "sector_multiplier": mult,
            "estimated_shock_pct": round(estimated_shock * 100, 2),
            "dollar_impact": round(dollar_impact, 2),
        })

    # Total portfolio impact
    total_impact = sum(
        investment_amount * weight_map[t] * asset_shocks[t] for t in tickers
    )
    new_value = investment_amount + total_impact

    return {
        "scenario": {
            "key": scenario_key,
            "name": scenario["name"],
            "description": scenario["description"],
            "market_drop_pct": round(market_drop * 100, 2),
        },
        "asset_impacts": asset_details,
        "portfolio_impact": {
            "original_value": investment_amount,
            "stressed_value": round(new_value, 2),
            "total_loss_dollar": round(total_impact, 2),
            "total_loss_pct": round((total_impact / investment_amount) * 100, 2),
        },
        "available_scenarios": list(STRESS_SCENARIOS.keys()),
    }
