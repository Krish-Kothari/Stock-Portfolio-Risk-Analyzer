"""
Portfolio routes — ticker validation.
"""

from flask import Blueprint, request, jsonify
from services.data_service import validate_tickers

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/api/portfolio")


@portfolio_bp.route("/validate", methods=["POST"])
def validate():
    """
    POST /api/portfolio/validate
    Body: { "tickers": ["AAPL", "GOOGL", "INVALID"] }
    Returns: { "valid": [...], "invalid": [...] }
    """
    data = request.get_json(force=True)
    tickers = data.get("tickers")

    if not tickers or not isinstance(tickers, list):
        return jsonify({"error": "A 'tickers' list is required."}), 400

    result = validate_tickers(tickers)
    return jsonify(result)
