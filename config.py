"""
Application Configuration
Contains trading parameters, strategies, and stock lists
"""
from env import API_KEY, API_SECRET

# Trading Configuration
INITIAL_CAPITAL = 100000  # Initial capital (₹)
DEFAULT_SYMBOL = "RELIANCE"  # Symbol for backtesting
USE_MOCK_DATA = False  # Use real Groww API data

# Available stocks for backtesting
AVAILABLE_STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries"},
    {"symbol": "TCS", "name": "TCS"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank"},
    {"symbol": "INFY", "name": "Infosys"},
    {"symbol": "ICICIBANK", "name": "ICICI Bank"},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever"},
    {"symbol": "SBIN", "name": "State Bank of India"},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel"},
    {"symbol": "ITC", "name": "ITC"},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank"},
    {"symbol": "VEDL", "name": "Vedanta Ltd"}
]

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
DEFAULT_MARGIN = "1x"  # 1x, 2x, 5x, or 10x leverage
