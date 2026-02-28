"""
Simulation routes — Monte Carlo simulation endpoint.
"""

from flask import Blueprint, request, jsonify
from services.monte_carlo import run_monte_carlo
from config import (
    DEFAULT_PERIOD,
    DEFAULT_NUM_SIMULATIONS,
    DEFAULT_SIMULATION_DAYS,
    DEFAULT_CONFIDENCE_LEVEL,
)

simulation_bp = Blueprint("simulation", __name__, url_prefix="/api/simulate")


@simulation_bp.route("/monte-carlo", methods=["POST"])
def monte_carlo():
    """
    POST /api/simulate/monte-carlo
    Run Monte Carlo simulation for the portfolio.
    """
    data = request.get_json(force=True)

    holdings = data.get("holdings")
    if not holdings or not isinstance(holdings, list):
        return jsonify({"error": "A 'holdings' list is required."}), 400

    for h in holdings:
        if "ticker" not in h or "weight" not in h:
            return jsonify({"error": "Each holding must have 'ticker' and 'weight'."}), 400

    total_weight = sum(h["weight"] for h in holdings)
    if not (0.99 <= total_weight <= 1.01):
        return jsonify({"error": f"Weights must sum to 1.0 (currently {total_weight:.4f})."}), 400

    period = data.get("period", DEFAULT_PERIOD)
    num_simulations = data.get("num_simulations", DEFAULT_NUM_SIMULATIONS)
    num_days = data.get("num_days", DEFAULT_SIMULATION_DAYS)
    investment = data.get("investment_amount", 100_000)
    confidence = data.get("confidence_level", DEFAULT_CONFIDENCE_LEVEL)

    # Cap simulations to avoid server overload
    num_simulations = min(num_simulations, 50_000)
    num_days = min(num_days, 504)  # max ~2 years

    try:
        result = run_monte_carlo(
            holdings=holdings,
            period=period,
            num_simulations=num_simulations,
            num_days=num_days,
            investment_amount=investment,
            confidence_level=confidence,
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Simulation failed: {str(e)}"}), 500
