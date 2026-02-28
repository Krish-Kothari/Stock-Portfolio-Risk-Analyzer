"""
Configuration for the Stock Portfolio Risk Analyzer.
"""

# --- Market Defaults ---
RISK_FREE_RATE = 0.0425          # US 10-Year Treasury yield (~4.25%)
TRADING_DAYS_PER_YEAR = 252      # Standard trading days in a year
BENCHMARK_TICKER = "^GSPC"       # S&P 500

# --- VaR Defaults ---
DEFAULT_CONFIDENCE_LEVEL = 0.95  # 95% confidence
CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]

# --- Monte Carlo Defaults ---
DEFAULT_NUM_SIMULATIONS = 10000
DEFAULT_SIMULATION_DAYS = 252    # 1 year forward

# --- Data Defaults ---
DEFAULT_PERIOD = "2y"            # 2 years of historical data
VALID_PERIODS = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"]

# --- Historical Stress Test Scenarios ---
STRESS_SCENARIOS = {
    "2008_crisis": {
        "name": "2008 Financial Crisis",
        "description": "Global financial meltdown triggered by subprime mortgage collapse",
        "market_drop": -0.565,    # S&P 500 peak-to-trough ~56.5%
        "sector_multipliers": {
            "financials": 1.8,
            "tech": 1.2,
            "healthcare": 0.7,
            "consumer": 1.1,
            "energy": 1.4,
            "default": 1.0,
        },
    },
    "covid_crash": {
        "name": "COVID-19 Crash (2020)",
        "description": "Rapid market sell-off due to global pandemic",
        "market_drop": -0.339,    # S&P 500 drop ~33.9%
        "sector_multipliers": {
            "travel": 2.0,
            "energy": 1.8,
            "tech": 0.6,
            "healthcare": 0.5,
            "consumer": 1.3,
            "default": 1.0,
        },
    },
    "dot_com_bust": {
        "name": "Dot-Com Bust (2000-2002)",
        "description": "Technology bubble collapse",
        "market_drop": -0.49,     # S&P 500 drop ~49%
        "sector_multipliers": {
            "tech": 2.2,
            "financials": 0.8,
            "healthcare": 0.5,
            "energy": 0.6,
            "default": 1.0,
        },
    },
    "2022_bear": {
        "name": "2022 Bear Market",
        "description": "Interest rate hikes and inflation-driven sell-off",
        "market_drop": -0.254,    # S&P 500 drop ~25.4%
        "sector_multipliers": {
            "tech": 1.5,
            "crypto": 2.5,
            "energy": 0.3,
            "healthcare": 0.7,
            "default": 1.0,
        },
    },
}
STRESS_SCENARIOS.update({
    "future_pandemic": {
        "name": "Future Pandemic",
        "description": "Hypothetical global health crisis: travel plummets, healthcare & tech resist",
        "market_drop": -0.30,
        "sector_multipliers": {
            "travel": 2.5,      # travel stocks drop 2.5x market
            "healthcare": -0.5,  # healthcare rises (negative = opposite direction)
            "tech": 0.8,
            "consumer": 1.5,
            "energy": 1.2,
            "default": 1.0,
        },
    },
    "ai_boom": {
        "name": "AI Revolution",
        "description": "Tech-led growth, automation surge: tech soars, energy lags",
        "market_drop": 0.20,     # positive market move
        "sector_multipliers": {
            "tech": -1.5,        # tech rises 1.5x market (negative amplifies positive)
            "energy": 0.5,
            "healthcare": 0.3,
            "financials": 0.8,
            "default": 1.0,
        },
    },
    "rate_cut_rally": {
        "name": "Rate Cut Rally",
        "description": "Fed cuts rates: growth stocks surge, utilities flat",
        "market_drop": 0.15,
        "sector_multipliers": {
            "tech": -1.8,
            "financials": 0.6,
            "realestate": -1.2,
            "utilities": 0.2,
            "default": 1.0,
        },
    },
})
