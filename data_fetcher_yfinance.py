import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def generate_mock_data(days=365, seed=42):
    """Generate mock stock data for testing"""
    np.random.seed(seed)
    
    dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
    base_price = 20000
    trend = np.linspace(0, 2000, days)
    noise = np.random.normal(0, 500, days)
    prices = base_price + trend + noise
    
    data = []
    for i, date in enumerate(dates):
        close = max(1000, prices[i])
        high = close * (1 + np.random.uniform(0, 0.02))
        low = close * (1 - np.random.uniform(0, 0.02))
        open_price = low + (high - low) * np.random.uniform(0.3, 0.7)
        volume = np.random.randint(1000000, 10000000)
        
        data.append({
            'timestamp': date,
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })
    
    return pd.DataFrame(data)

def fetch_historical_data(symbol, exchange="NSE", interval="1d", use_mock=False):
    """
    Fetch historical data from Yahoo Finance
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "INFY")
        exchange: Exchange name (default: "NSE")
        interval: Time interval (default: "1d")
        use_mock: If True, use mock data instead of API
    
    Returns:
        pandas.DataFrame with columns: timestamp, open, high, low, close, volume
    """
    if use_mock:
        print(f"Using mock data for {symbol}")
        return generate_mock_data()
    
    try:
        # Add .NS suffix for NSE stocks
        if exchange == "NSE" and not symbol.endswith(".NS"):
            yf_symbol = f"{symbol}.NS"
        else:
            yf_symbol = symbol
        
        print(f"Fetching {symbol} data from Yahoo Finance...")
        
        # Download data for last 365 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
        
        # Rename columns to match our format
        df = df.reset_index()
        df = df.rename(columns={
            'Date': 'timestamp',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        # Select only required columns
        df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
        # Sort by timestamp
        df = df.sort_values("timestamp").reset_index(drop=True)
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        print(f"✅ Successfully fetched {len(df)} data points for {symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error fetching data from Yahoo Finance: {str(e)}")
        print(f"Falling back to mock data for {symbol}")
        return generate_mock_data()
