from config import INITIAL_CAPITAL, DEFAULT_SYMBOL, USE_MOCK_DATA
from data_fetcher import fetch_historical_data
from strategy import calculate_indicators, generate_signals
from backtest import backtest_strategy
from visualization import plot_strategy

def main():
    symbol = DEFAULT_SYMBOL
    df = fetch_historical_data(symbol, use_mock=USE_MOCK_DATA)
    df = calculate_indicators(df)
    df = generate_signals(df)

    final_value, pnl, trades = backtest_strategy(df, INITIAL_CAPITAL)

    print("Final Portfolio Value:", round(final_value, 2))
    print("Net P&L:", round(pnl, 2))
    print("Total Trades:", len(trades))

    plot_strategy(df, symbol)

if __name__ == "__main__":
    main()
