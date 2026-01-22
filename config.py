# Groww API Configuration (Key + Secret)
# Get these from Groww Developer Portal. Use key_type "approval".
API_KEY = "key"
API_SECRET = "secret"

# Trading Configuration
INITIAL_CAPITAL = 100000  # Initial capital (₹)
DEFAULT_SYMBOL = "VEDL"  # Symbol for backtesting
USE_MOCK_DATA = False  # Use real Groww API data

# Strategies: display name -> functions in strategy.py (indicators, signals)
STRATEGIES = {
    "SMA Crossover": {
        "indicators": "calculate_indicators",
        "signals": "generate_signals",
    },
    "RSI Oversold": {
        "indicators": "rsi_indicators",
        "signals": "rsi_signals",
        "exit_rules": {"take_profit_rs": 10, "hold_max_days": 1},
    },
    "VWAP Trend Rider": {
        "indicators": "vwap_indicators",
        "signals": "vwap_trend_rider_signals",
    },
    "VWAP + EMA Confluence": {
        "indicators": "vwap_indicators",
        "signals": "vwap_ema_confluence_signals",
    },
}
DEFAULT_STRATEGY = "SMA Crossover"
DEFAULT_MARGIN = "2x"  # 2x, 5x, or 10x leverage
