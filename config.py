# Groww API Configuration (Key + Secret)
# Get these from Groww Developer Portal. Use key_type "approval".
API_KEY = "eyJraWQiOiJaTUtjVXciLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjI1NTc1MTQ3OTMsImlhdCI6MTc2OTExNDc5MywibmJmIjoxNzY5MTE0NzkzLCJzdWIiOiJ7XCJ0b2tlblJlZklkXCI6XCIzOTM4OWJmNS1iODQ2LTRlNWYtOWQxYi1jMzUzMTViMmI4MTVcIixcInZlbmRvckludGVncmF0aW9uS2V5XCI6XCJlMzFmZjIzYjA4NmI0MDZjODg3NGIyZjZkODQ5NTMxM1wiLFwidXNlckFjY291bnRJZFwiOlwiNzcyZTFjODctMGI0ZC00OTMxLTk2MDktZjRmZTA5YjA1MGY3XCIsXCJkZXZpY2VJZFwiOlwiZDU3ZTBjNGQtOTVmOS01ZjllLWI2ZjgtMDMyMmM4ZjViMGUyXCIsXCJzZXNzaW9uSWRcIjpcImE1YWVkMGI4LTU4YTItNDEwMi04N2FhLTJmZjFiZTczYTk4NlwiLFwiYWRkaXRpb25hbERhdGFcIjpcIno1NC9NZzltdjE2WXdmb0gvS0EwYktXeFVXSDNEQTBFbDBoYjBETFBtUk5STkczdTlLa2pWZDNoWjU1ZStNZERhWXBOVi9UOUxIRmtQejFFQisybTdRPT1cIixcInJvbGVcIjpcImF1dGgtdG90cFwiLFwic291cmNlSXBBZGRyZXNzXCI6XCIyNDA1OjIwMTo2ODBjOjgxN2Y6NTk2NzplMWI2OjY5OTE6OGIyZCwxNzIuNjkuMTE5LjEwMywzNS4yNDEuMjMuMTIzXCIsXCJ0d29GYUV4cGlyeVRzXCI6MjU1NzUxNDc5MzI1NX0iLCJpc3MiOiJhcGV4LWF1dGgtcHJvZC1hcHAifQ.dDH4c4phl43LTS2sYg2YvjHe2tozTN03_RVTaH3OcWN_m6_wCvkClwsZu3RZzT1xMzpV88lJK3Imvh3r7TTtkQ"
API_SECRET = "oFk@8qiN)oC6rDDo#CXB$(TB_DBf^LJt"

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
DEFAULT_MARGIN = "2x"  # 2x, 5x, or 10x leverage
