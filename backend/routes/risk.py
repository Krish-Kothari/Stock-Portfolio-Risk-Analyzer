"""
Risk routes — full dashboard, correlation matrix, per-asset breakdown.
"""

from flask import Blueprint, request, jsonify
from services.risk_engine import (
    compute_all_metrics,
    compute_correlation_matrix,
    compute_individual_risk,
)
from config import DEFAULT_PERIOD, DEFAULT_CONFIDENCE_LEVEL, RISK_FREE_RATE

risk_bp = Blueprint("risk", __name__, url_prefix="/api/risk")


def _parse_holdings(data: dict) -> tuple:
    """Extract and validate common fields from request body."""
    holdings = data.get("holdings")
    if not holdings or not isinstance(holdings, list):
        return None, None, None, None, "A 'holdings' list is required."

    for h in holdings:
        if "ticker" not in h or "weight" not in h:
            return None, None, None, None, "Each holding must have 'ticker' and 'weight'."

    # Validate weights sum ≈ 1.0
    total_weight = sum(h["weight"] for h in holdings)
    if not (0.99 <= total_weight <= 1.01):
        return None, None, None, None, (
            f"Weights must sum to 1.0 (currently {total_weight:.4f})."
        )

    period = data.get("period", DEFAULT_PERIOD)
    confidence = data.get("confidence_level", DEFAULT_CONFIDENCE_LEVEL)
    investment = data.get("investment_amount", 100_000)

    return holdings, period, confidence, investment, None


@risk_bp.route("/metrics", methods=["POST"])
def metrics():
    """
    POST /api/risk/metrics
    Full risk dashboard for the portfolio.
    """
    data = request.get_json(force=True)
    holdings, period, confidence, investment, err = _parse_holdings(data)
    if err:
        return jsonify({"error": err}), 400

    risk_free = data.get("risk_free_rate", RISK_FREE_RATE)

    try:
        result = compute_all_metrics(
            holdings=holdings,
            period=period,
            confidence=confidence,
            risk_free_rate=risk_free,
            investment_amount=investment,
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Computation failed: {str(e)}"}), 500


@risk_bp.route("/correlation", methods=["POST"])
def correlation():
    """
    POST /api/risk/correlation
    Correlation and covariance matrices.
    """
    data = request.get_json(force=True)
    holdings = data.get("holdings")
    if not holdings:
        return jsonify({"error": "A 'holdings' list is required."}), 400

    period = data.get("period", DEFAULT_PERIOD)

    try:
        result = compute_correlation_matrix(holdings, period)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Computation failed: {str(e)}"}), 500


@risk_bp.route("/individual", methods=["POST"])
def individual():
    """
    POST /api/risk/individual
    Per-asset risk breakdown.
    """
    data = request.get_json(force=True)
    holdings, period, confidence, _, err = _parse_holdings(data)
    if err:
        return jsonify({"error": err}), 400

    risk_free = data.get("risk_free_rate", RISK_FREE_RATE)

    try:
        result = compute_individual_risk(
            holdings=holdings,
            period=period,
            confidence=confidence,
            risk_free_rate=risk_free,
        )
        return jsonify({"assets": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Computation failed: {str(e)}"}), 500