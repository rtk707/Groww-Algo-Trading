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
