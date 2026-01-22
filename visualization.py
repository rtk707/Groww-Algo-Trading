import matplotlib.pyplot as plt

def plot_strategy(df, symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["close"], label="Price")
    plt.plot(df["timestamp"], df["SMA_20"], label="SMA 20")
    plt.plot(df["timestamp"], df["SMA_50"], label="SMA 50")
    plt.title(f"SMA Crossover Strategy - {symbol}")
    plt.legend()
    plt.show()
