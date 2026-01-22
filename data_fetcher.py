import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from growwapi import GrowwAPI
from config import API_KEY, API_SECRET

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
    Fetch historical data from Groww API
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS", "INFY")
        exchange: Exchange name (default: "NSE")
        interval: Time interval (default: "1d" for daily)
        use_mock: If True, use mock data instead of API
    
    Returns:
        pandas.DataFrame with columns: timestamp, open, high, low, close, volume
    """
    if use_mock:
        print(f"Using mock data for {symbol}")
        return generate_mock_data()
    
    try:
        # Groww expects plain symbols (e.g. RELIANCE), strip .NS/.BO if present
        groww_symbol = symbol.split(".")[0] if "." in symbol else symbol
        
        # Obtain access token from API key + secret
        token = GrowwAPI.get_access_token(API_KEY, secret=API_SECRET)
        groww = GrowwAPI(token)
        
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        
        interval_map = {
            "1m": 1,
            "5m": 5,
            "15m": 15,
            "30m": 30,
            "1h": 60,
            "1d": 1440,
        }
        interval_minutes = interval_map.get(interval, 1440)
        
        print(f"Fetching {groww_symbol} data from Groww API...")
        
        response = groww.get_historical_candle_data(
            trading_symbol=groww_symbol,
            exchange=groww.EXCHANGE_NSE,
            segment=groww.SEGMENT_CASH,
            start_time=start_time,
            end_time=end_time,
            interval_in_minutes=interval_minutes
        )
        
        if not response or "candles" not in response:
            raise ValueError(f"Invalid response from Groww API for {groww_symbol}")
        
        candles = response["candles"]
        if not candles or len(candles) == 0:
            raise ValueError(f"No data returned for {groww_symbol}")
        
        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
        df = df.sort_values("timestamp").reset_index(drop=True)
        
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna()
        
        if len(df) == 0:
            raise ValueError(f"No valid data after cleaning for {groww_symbol}")
        
        print(f"✅ Successfully fetched {len(df)} data points for {groww_symbol}")
        return df
        
    except Exception as e:
        print(f"❌ Error fetching data from Groww API for {symbol}: {str(e)}")
        print(f"Falling back to mock data for {symbol}")
        return generate_mock_data()
