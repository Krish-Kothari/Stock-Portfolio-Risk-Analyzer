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


@portfolio_bp.route("/live-prices", methods=["GET"])
def live_prices():
    """
    GET /api/portfolio/live-prices?tickers=AAPL,MSFT,GOOGL
    Returns live prices and daily changes for the marquee.
    """
    tickers_param = request.args.get("tickers", "AAPL,MSFT,GOOGL,NVDA,TSLA,AMZN")
    tickers = [t.strip().upper() for t in tickers_param.split(",") if t.strip()]
    
    from services.data_service import fetch_live_prices
    data = fetch_live_prices(tickers)
    return jsonify({"prices": data})
