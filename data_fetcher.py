import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from growwapi import GrowwAPI
from config import API_AUTH_TOKEN

def generate_mock_data(days=365, seed=42):
    """Generate mock stock data for testing
    
    Args:
        days: Number of days of data to generate
        seed: Random seed for reproducibility
    """
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
    Fetch historical data from Groww API or use mock data
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "INFY")
        exchange: Exchange name (default: "NSE")
        interval: Time interval (default: "1d" for daily data)
        use_mock: If True, use mock data instead of API
    
    Returns:
        pandas.DataFrame with columns: timestamp, open, high, low, close, volume
    """
    if use_mock:
        print(f"Using mock data for {symbol}")
        return generate_mock_data()
    
    try:
        # Initialize Groww API
        groww = GrowwAPI(API_AUTH_TOKEN)
        
        # Calculate date range (last 365 days)
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Convert interval to minutes
        interval_map = {
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "1h": 60,
            "1d": 1440,  # Daily
        }
        interval_minutes = interval_map.get(interval, 1440)
        
        print(f"Fetching {symbol} data from Groww API...")
        
        # Fetch historical candle data
        response = groww.get_historical_candle_data(
            trading_symbol=symbol,
            exchange=groww.EXCHANGE_NSE,
            segment=groww.SEGMENT_CASH,
            start_time=start_time,
            end_time=end_time,
            interval_in_minutes=interval_minutes
        )
        
        # Parse response
        if not response or "candles" not in response:
            raise ValueError(f"Invalid response from Groww API for {symbol}")
        
        candles = response["candles"]
        if not candles or len(candles) == 0:
            raise ValueError(f"No data returned for {symbol}")
        
        # Convert to DataFrame
        # Format: [timestamp_epoch, open, high, low, close, volume]
        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        
        # Convert epoch timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
        
        # Sort by timestamp
        df = df.sort_values("timestamp").reset_index(drop=True)
        
        # Ensure numeric columns
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        print(f"✅ Successfully fetched {len(df)} data points for {symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error fetching data from Groww API: {str(e)}")
        print(f"Falling back to mock data for {symbol}")
        return generate_mock_data()
