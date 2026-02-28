"""
Scenario routes — shock analysis and historical stress tests.
"""

from flask import Blueprint, request, jsonify
from services.scenario import shock_analysis, stress_test
from config import DEFAULT_PERIOD, DEFAULT_CONFIDENCE_LEVEL, STRESS_SCENARIOS

scenario_bp = Blueprint("scenario", __name__, url_prefix="/api/scenario")


def _parse_base(data: dict) -> tuple:
    """Extract common fields."""
    holdings = data.get("holdings")
    if not holdings or not isinstance(holdings, list):
        return None, None, None, None, "A 'holdings' list is required."

    for h in holdings:
        if "ticker" not in h or "weight" not in h:
            return None, None, None, None, "Each holding must have 'ticker' and 'weight'."

    total_weight = sum(h["weight"] for h in holdings)
    if not (0.99 <= total_weight <= 1.01):
        return None, None, None, None, (
            f"Weights must sum to 1.0 (currently {total_weight:.4f})."
        )

    period = data.get("period", DEFAULT_PERIOD)
    confidence = data.get("confidence_level", DEFAULT_CONFIDENCE_LEVEL)
    investment = data.get("investment_amount", 100_000)

    return holdings, period, confidence, investment, None


@scenario_bp.route("/shock", methods=["POST"])
def shock():
    """
    POST /api/scenario/shock
    Body: { "holdings": [...], "shocks": {"AAPL": -0.20}, ... }
    """
    data = request.get_json(force=True)
    holdings, period, confidence, investment, err = _parse_base(data)
    if err:
        return jsonify({"error": err}), 400

    shocks = data.get("shocks")
    if not shocks or not isinstance(shocks, dict):
        return jsonify({"error": "A 'shocks' dict is required, e.g. {\"AAPL\": -0.20}"}), 400

    try:
        result = shock_analysis(
            holdings=holdings,
            shocks=shocks,
            period=period,
            confidence=confidence,
            investment_amount=investment,
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@scenario_bp.route("/stress-test", methods=["POST"])
def stress():
    """
    POST /api/scenario/stress-test
    Body: { "holdings": [...], "scenario": "2008_crisis" }
    """
    data = request.get_json(force=True)
    holdings, period, confidence, investment, err = _parse_base(data)
    if err:
        return jsonify({"error": err}), 400

    scenario_key = data.get("scenario")
    if not scenario_key:
        return jsonify({
            "error": "A 'scenario' key is required.",
            "available_scenarios": list(STRESS_SCENARIOS.keys()),
        }), 400

    try:
        result = stress_test(
            holdings=holdings,
            scenario_key=scenario_key,
            period=period,
            confidence=confidence,
            investment_amount=investment,
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Stress test failed: {str(e)}"}), 500
