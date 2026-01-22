def calculate_indicators(df):
    df["SMA_20"] = df["close"].rolling(20).mean()
    df["SMA_50"] = df["close"].rolling(50).mean()
    return df


def generate_signals(df):
    df["signal"] = 0
    df.loc[df["SMA_20"] > df["SMA_50"], "signal"] = 1
    df.loc[df["SMA_20"] < df["SMA_50"], "signal"] = -1
    df["position"] = df["signal"].shift(1)
    return df


def rsi_indicators(df, period=14):
    """Compute RSI (Relative Strength Index)."""
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-10)
    df["RSI"] = 100 - (100 / (1 + rs))
    return df


def rsi_signals(df, buy_thresh=20):
    """
    Buy when RSI < buy_thresh (oversold).
    Sell is handled by backtest exit rules: +₹10 gain or EOD (hold max 1 day).
    """
    df["signal"] = 0
    df.loc[df["RSI"] < buy_thresh, "signal"] = 1
    df["position"] = df["signal"].shift(1)
    return df


# --- VWAP (Volume Weighted Average Price) ---
# Rolling VWAP over window. Typical price = (H+L+C)/3.
# Trade with the trend: above VWAP = buyers in control, below = sellers.


def vwap_indicators(df, window=20, ema_fast=9, ema_slow=20):
    """Compute rolling VWAP and EMAs for VWAP strategies."""
    tp = (df["high"] + df["low"] + df["close"]) / 3
    pv = tp * df["volume"]
    df["VWAP"] = pv.rolling(window).sum() / df["volume"].rolling(window).sum()
    df["EMA_9"] = df["close"].ewm(span=ema_fast, adjust=False).mean()
    df["EMA_20"] = df["close"].ewm(span=ema_slow, adjust=False).mean()
    return df


def vwap_trend_rider_signals(df):
    """
    VWAP Trend Rider (Strategy 1): Trade in direction of price vs VWAP.
    Long: Price above VWAP, pullback to VWAP or EMA, bullish candle. Buy continuation.
    Sell: Price drops below VWAP (buyers lose control).
    """
    df["signal"] = 0
    above_vwap = df["close"] > df["VWAP"]
    bullish = df["close"] > df["open"]
    near_vwap = (df["low"] <= df["VWAP"] * 1.005) & (df["low"] >= df["VWAP"] * 0.995)
    near_ema = (df["low"] <= df["EMA_9"] * 1.005) & (df["low"] >= df["EMA_9"] * 0.995)
    pullback = near_vwap | near_ema
    buy = above_vwap & bullish & pullback
    df.loc[buy, "signal"] = 1
    df.loc[~above_vwap & (df["signal"] != 1), "signal"] = -1
    df["position"] = df["signal"].shift(1)
    return df


def vwap_ema_confluence_signals(df):
    """
    VWAP + EMA Confluence (Strategy 3): Algo-friendly filter.
    Long: Price > VWAP, 9 EMA > 20 EMA, pullback doesn't break VWAP, entry on EMA bounce.
    Sell: Price < VWAP or 9 EMA < 20 EMA.
    """
    df["signal"] = 0
    above_vwap = df["close"] > df["VWAP"]
    ema_bull = df["EMA_9"] > df["EMA_20"]
    no_break = df["low"] > df["VWAP"]
    prev_below = df["close"].shift(1) <= df["EMA_9"].shift(1)
    curr_above = df["close"] > df["EMA_9"]
    bounce = prev_below & curr_above
    buy = above_vwap & ema_bull & no_break & bounce
    df.loc[buy, "signal"] = 1
    sell_cond = ~above_vwap | ~ema_bull
    df.loc[sell_cond & (df["signal"] != 1), "signal"] = -1
    df["position"] = df["signal"].shift(1)
    return df
