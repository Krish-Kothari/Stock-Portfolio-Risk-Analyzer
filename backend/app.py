"""
Stock Portfolio Risk Analyzer — Flask Application Entry Point
"""

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from routes.portfolio import portfolio_bp
from routes.risk import risk_bp
from routes.simulation import simulation_bp
from routes.scenario import scenario_bp


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # allow cross-origin from any frontend

    # --- Register blueprints ---
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(simulation_bp)
    app.register_blueprint(scenario_bp)

    # --- Health-check / index ---
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/health")
    def health():
        return jsonify({
            "service": "Stock Portfolio Risk Analyzer API",
            "version": "1.0.0",
            "endpoints": {
                "portfolio": {
                    "POST /api/portfolio/validate": "Validate stock tickers",
                },
                "risk": {
                    "POST /api/risk/metrics": "Full risk dashboard",
                    "POST /api/risk/correlation": "Correlation & covariance matrices",
                    "POST /api/risk/individual": "Per-asset risk breakdown",
                },
                "simulation": {
                    "POST /api/simulate/monte-carlo": "Monte Carlo simulation",
                },
                "scenario": {
                    "POST /api/scenario/shock": "What-if shock analysis",
                    "POST /api/scenario/stress-test": "Historical stress test",
                },
            },
        })

    # --- Global error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error."}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
