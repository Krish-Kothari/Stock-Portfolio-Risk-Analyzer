"""
Monte Carlo Simulation Engine — correlated Geometric Brownian Motion
using Cholesky decomposition for realistic multi-asset simulation.
"""

import numpy as np
import pandas as pd

from config import (
    DEFAULT_NUM_SIMULATIONS,
    DEFAULT_SIMULATION_DAYS,
    TRADING_DAYS_PER_YEAR,
    DEFAULT_CONFIDENCE_LEVEL,
    DEFAULT_PERIOD,
)
from services.data_service import fetch_prices, compute_returns


def run_monte_carlo(
    holdings: list[dict],
    period: str = DEFAULT_PERIOD,
    num_simulations: int = DEFAULT_NUM_SIMULATIONS,
    num_days: int = DEFAULT_SIMULATION_DAYS,
    investment_amount: float = 100_000,
    confidence_level: float = DEFAULT_CONFIDENCE_LEVEL,
) -> dict:
    """
    Run a Monte Carlo simulation for the portfolio.

    Uses correlated GBM via Cholesky decomposition of the asset
    covariance matrix, producing *num_simulations* possible future
    paths over *num_days* trading days.

    Returns a JSON-serialisable dict with:
      - percentile_paths (5th / 25th / 50th / 75th / 95th)
      - terminal_value stats
      - VaR from simulation
      - probability of loss
    """
    tickers = [h["ticker"] for h in holdings]
    weights = np.array([h["weight"] for h in holdings])

    # --- Historical data ---
    prices = fetch_prices(tickers, period)
    returns = compute_returns(prices)[tickers]

    mean_daily = returns.mean().values                       # (n,)
    cov_daily = returns.cov().values                         # (n, n)
    n_assets = len(tickers)

    # --- Cholesky decomposition for correlated random draws ---
    try:
        L = np.linalg.cholesky(cov_daily)
    except np.linalg.LinAlgError:
        # If the matrix is not positive-definite, add a tiny regulariser
        cov_daily += np.eye(n_assets) * 1e-10
        L = np.linalg.cholesky(cov_daily)

    # --- Simulate ---
    # Shape: (num_simulations, num_days)
    portfolio_paths = np.zeros((num_simulations, num_days + 1))
    portfolio_paths[:, 0] = investment_amount

    for sim in range(num_simulations):
        # Correlated random daily returns for all days at once
        Z = np.random.standard_normal((num_days, n_assets))
        correlated_returns = Z @ L.T + mean_daily  # (num_days, n_assets)

        # Portfolio daily return is the weighted sum
        port_daily = correlated_returns @ weights  # (num_days,)

        # Build cumulative path
        cum = np.cumprod(1 + port_daily)
        portfolio_paths[sim, 1:] = investment_amount * cum

    # --- Statistics ---
    terminal_values = portfolio_paths[:, -1]

    # Percentile paths
    pct_labels = [5, 25, 50, 75, 95]
    percentile_paths = {}
    for p in pct_labels:
        percentile_paths[f"p{p}"] = np.percentile(
            portfolio_paths, p, axis=0
        ).tolist()

    # Daily portfolio returns from paths
    sim_returns = np.diff(portfolio_paths, axis=1) / portfolio_paths[:, :-1]
    all_daily_returns = sim_returns.flatten()

    # Monte Carlo VaR
    mc_var = float(-np.percentile(all_daily_returns, (1 - confidence_level) * 100))
    mc_var_dollar = mc_var * investment_amount

    # Probability of loss
    prob_loss = float(np.mean(terminal_values < investment_amount))

    # Terminal value distribution
    terminal_stats = {
        "mean": round(float(np.mean(terminal_values)), 2),
        "median": round(float(np.median(terminal_values)), 2),
        "std": round(float(np.std(terminal_values)), 2),
        "min": round(float(np.min(terminal_values)), 2),
        "max": round(float(np.max(terminal_values)), 2),
        "p5": round(float(np.percentile(terminal_values, 5)), 2),
        "p25": round(float(np.percentile(terminal_values, 25)), 2),
        "p75": round(float(np.percentile(terminal_values, 75)), 2),
        "p95": round(float(np.percentile(terminal_values, 95)), 2),
    }

    # Subsample paths for response size (max 200 paths for charting)
    sample_count = min(200, num_simulations)
    indices = np.random.choice(num_simulations, sample_count, replace=False)
    sampled_paths = portfolio_paths[indices].tolist()

    return {
        "simulation_params": {
            "num_simulations": num_simulations,
            "num_days": num_days,
            "investment_amount": investment_amount,
            "confidence_level": confidence_level,
            "tickers": tickers,
            "weights": weights.tolist(),
        },
        "percentile_paths": percentile_paths,
        "terminal_value_stats": terminal_stats,
        "monte_carlo_var": {
            "var_1d": round(mc_var, 6),
            "var_1d_pct": round(mc_var * 100, 4),
            "var_1d_dollar": round(mc_var_dollar, 2),
        },
        "probability_of_loss": round(prob_loss, 4),
        "probability_of_loss_pct": round(prob_loss * 100, 2),
        "sampled_paths": sampled_paths,
        "days": list(range(num_days + 1)),
    }
