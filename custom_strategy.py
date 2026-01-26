"""
Custom Strategy Executor
Allows users to define their own trading strategies with conditions on indicators
"""
import pandas as pd
import numpy as np


def compute_all_indicators(df):
    """Compute all available indicators that users can use in custom strategies"""
    # SMA
    df["SMA_20"] = df["close"].rolling(20).mean()
    df["SMA_50"] = df["close"].rolling(50).mean()
    df["SMA_100"] = df["close"].rolling(100).mean()
    df["SMA_200"] = df["close"].rolling(200).mean()
    
    # RSI
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-10)
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # VWAP
    tp = (df["high"] + df["low"] + df["close"]) / 3
    pv = tp * df["volume"]
    df["VWAP"] = pv.rolling(20).sum() / df["volume"].rolling(20).sum()
    
    # EMA
    df["EMA_9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["EMA_20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["EMA_100"] = df["close"].ewm(span=100, adjust=False).mean()
    df["EMA_200"] = df["close"].ewm(span=200, adjust=False).mean()
    
    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Histogram"] = df["MACD"] - df["MACD_Signal"]
    
    # Bollinger Bands
    bb_period = 20
    bb_std = 2
    df["BB_Middle"] = df["close"].rolling(bb_period).mean()
    bb_std_val = df["close"].rolling(bb_period).std()
    df["BB_Upper"] = df["BB_Middle"] + (bb_std_val * bb_std)
    df["BB_Lower"] = df["BB_Middle"] - (bb_std_val * bb_std)
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
    df["BB_Position"] = (df["close"] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])
    
    # Stochastic Oscillator
    stoch_k_period = 14
    stoch_d_period = 3
    low_min = df["low"].rolling(stoch_k_period).min()
    high_max = df["high"].rolling(stoch_k_period).max()
    df["Stoch_K"] = 100 * ((df["close"] - low_min) / (high_max - low_min))
    df["Stoch_D"] = df["Stoch_K"].rolling(stoch_d_period).mean()
    
    # ATR (Average True Range)
    atr_period = 14
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = true_range.rolling(atr_period).mean()
    
    # Volume indicators
    df["Volume_SMA"] = df["volume"].rolling(20).mean()
    df["Volume_Ratio"] = df["volume"] / df["Volume_SMA"].replace(0, 1e-10)
    
    # Price change indicators
    df["Price_Change"] = df["close"].pct_change() * 100
    df["Price_Change_5"] = df["close"].pct_change(5) * 100
    df["Price_Change_10"] = df["close"].pct_change(10) * 100
    
    # Price fields (for direct comparison)
    df["price"] = df["close"]
    df["open_price"] = df["open"]
    df["high_price"] = df["high"]
    df["low_price"] = df["low"]
    df["volume"] = df["volume"]
    
    return df


def evaluate_condition(df, condition):
    """
    Evaluate a single condition on the dataframe.
    
    condition format: {
        "indicator": "RSI",
        "operator": "<",
        "value": 20,
        "compare_to": "SMA_20"  # Optional: for indicator comparison
    }
    
    Supported operators:
    - Basic: <, <=, >, >=, ==, !=
    - Cross: crosses_above, crosses_below
    - Percentage: pct_change, pct_change_above, pct_change_below
    
    Returns: boolean Series
    """
    indicator = condition.get("indicator", "")
    operator = condition.get("operator", ">")
    value = condition.get("value")
    compare_to = condition.get("compare_to")  # For indicator comparison
    
    if indicator not in df.columns:
        return pd.Series([False] * len(df), index=df.index)
    
    col = df[indicator]
    
    # Indicator comparison (e.g., RSI > SMA_20)
    if compare_to and compare_to in df.columns:
        compare_col = df[compare_to]
        if operator == "<":
            return col < compare_col
        elif operator == "<=":
            return col <= compare_col
        elif operator == ">":
            return col > compare_col
        elif operator == ">=":
            return col >= compare_col
        elif operator == "==":
            return col == compare_col
        elif operator == "!=":
            return col != compare_col
        elif operator == "crosses_above":
            return (col > compare_col) & (col.shift(1) <= compare_col.shift(1))
        elif operator == "crosses_below":
            return (col < compare_col) & (col.shift(1) >= compare_col.shift(1))
        else:
            return pd.Series([False] * len(df), index=df.index)
    
    # Cross operators (crosses above/below a value)
    if operator == "crosses_above":
        if value is None:
            return pd.Series([False] * len(df), index=df.index)
        return (col > value) & (col.shift(1) <= value)
    elif operator == "crosses_below":
        if value is None:
            return pd.Series([False] * len(df), index=df.index)
        return (col < value) & (col.shift(1) >= value)
    
    # Percentage change operators
    if operator == "pct_change":
        if value is None:
            return pd.Series([False] * len(df), index=df.index)
        pct_change = col.pct_change() * 100
        return pct_change > value
    elif operator == "pct_change_above":
        if value is None:
            return pd.Series([False] * len(df), index=df.index)
        pct_change = col.pct_change() * 100
        return pct_change > value
    elif operator == "pct_change_below":
        if value is None:
            return pd.Series([False] * len(df), index=df.index)
        pct_change = col.pct_change() * 100
        return pct_change < value
    
    # Basic comparison operators
    if value is None:
        return pd.Series([False] * len(df), index=df.index)
    
    value = float(value)
    
    if operator == "<":
        return col < value
    elif operator == "<=":
        return col <= value
    elif operator == ">":
        return col > value
    elif operator == ">=":
        return col >= value
    elif operator == "==":
        return col == value
    elif operator == "!=":
        return col != value
    else:
        return pd.Series([False] * len(df), index=df.index)


def combine_conditions(df, conditions, logic="AND"):
    """
    Combine multiple conditions with AND or OR logic.
    
    conditions: list of condition dicts
    logic: "AND" or "OR"
    """
    if not conditions:
        return pd.Series([False] * len(df), index=df.index)
    
    results = [evaluate_condition(df, cond) for cond in conditions]
    
    if logic == "AND":
        combined = results[0]
        for r in results[1:]:
            combined = combined & r
        return combined
    else:  # OR
        combined = results[0]
        for r in results[1:]:
            combined = combined | r
        return combined


def execute_custom_strategy(df, buy_conditions, sell_conditions, buy_logic="AND", sell_logic="AND"):
    """
    Execute a custom strategy based on user-defined buy and sell conditions.
    
    Args:
        df: DataFrame with indicators computed
        buy_conditions: list of condition dicts for buy signal
        sell_conditions: list of condition dicts for sell signal
        buy_logic: "AND" or "OR" for combining buy conditions
        sell_logic: "AND" or "OR" for combining sell conditions
    
    Returns:
        DataFrame with 'signal' and 'position' columns
    """
    df = df.copy()
    df["signal"] = 0
    
    # Evaluate buy conditions
    if buy_conditions:
        buy_mask = combine_conditions(df, buy_conditions, buy_logic)
        df.loc[buy_mask, "signal"] = 1
    
    # Evaluate sell conditions
    if sell_conditions:
        sell_mask = combine_conditions(df, sell_conditions, sell_logic)
        df.loc[sell_mask, "signal"] = -1
    
    # Position is signal shifted by 1 (we act on next bar)
    df["position"] = df["signal"].shift(1)
    
    return df
