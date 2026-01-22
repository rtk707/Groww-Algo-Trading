# Groww Algo Trading System

Algorithmic trading backtesting system with real Groww API integration and web UI.

## Features
- ✅ Real market data from Groww API
- ✅ SMA crossover trading strategy
- ✅ Backtesting engine
- ✅ Web dashboard with interactive charts
- ✅ Mock data fallback for testing

## Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure API Key & Secret
Edit `config.py` and add your Groww API key and secret (from Groww Developer Portal):
```python
API_KEY = "your_groww_api_key_here"
API_SECRET = "your_groww_api_secret_here"
```

### 3. Run the Application

**Option A: Using the run script**
```bash
./run.sh  # macOS/Linux
run.bat   # Windows
```

**Option B: Manual start**
```bash
python3 app.py
```

### 4. Open Browser
Navigate to `http://localhost:5000` and click "Start Backtest"

## Configuration

Edit `config.py`:
- `API_KEY` - Your Groww API key
- `API_SECRET` - Your Groww API secret
- `DEFAULT_SYMBOL` - Stock symbol to backtest (e.g., "RELIANCE", "TCS", "INFY")
- `INITIAL_CAPITAL` - Starting capital (₹)
- `USE_MOCK_DATA` - Set to `False` for real data, `True` for mock data

## Strategy

**SMA Crossover:**
- Buy signal: SMA 20 crosses above SMA 50 (bullish)
- Sell signal: SMA 20 crosses below SMA 50 (bearish)
- Long-only positions
- All-in trading (uses full capital)

## Supported Symbols

NSE stocks like:
- RELIANCE
- TCS
- INFY (Infosys)
- HDFCBANK
- ICICIBANK
- And many more NSE stocks

## Files

- `app.py` - Flask web server
- `main.py` - CLI version
- `data_fetcher.py` - Data fetching via Groww API
- `strategy.py` - Trading strategy implementation
- `backtest.py` - Backtesting engine
- `config.py` - Configuration
- `templates/index.html` - Web UI
