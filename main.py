from config import (
    INITIAL_CAPITAL,
    DEFAULT_SYMBOL,
    USE_MOCK_DATA,
    STRATEGIES,
    DEFAULT_STRATEGY,
    DEFAULT_MARGIN,
)
from data_fetcher import fetch_historical_data
import strategy as strategy_module
from backtest import backtest_strategy


def main():
    symbol = DEFAULT_SYMBOL
    strategy_id = DEFAULT_STRATEGY
    cfg = STRATEGIES[strategy_id]
    calc_fn = getattr(strategy_module, cfg["indicators"])
    signal_fn = getattr(strategy_module, cfg["signals"])

    df = fetch_historical_data(symbol, use_mock=USE_MOCK_DATA)
    df = calc_fn(df)
    df = signal_fn(df)

    exit_rules = cfg.get("exit_rules")
    leverage_map = {"1x": 1, "2x": 2, "5x": 5, "10x": 10}
    leverage = leverage_map.get(DEFAULT_MARGIN.strip(), 1)
    final_value, pnl, trades = backtest_strategy(
        df, INITIAL_CAPITAL, exit_rules=exit_rules, leverage=leverage, stop_loss_pct=0.10
    )

    print(f"Strategy: {strategy_id} | Margin: {DEFAULT_MARGIN} | 10% stop-loss")
    print(f"Final Portfolio Value: ₹{round(final_value, 2):,.2f}")
    print(f"Net P&L: ₹{round(pnl, 2):,.2f}")
    print(f"Return: {round((pnl / INITIAL_CAPITAL) * 100, 2)}%")
    print(f"Total Trades: {len(trades)}")
    
    if trades:
        print("\nTrade History:")
        for trade in trades:
            print(f"  {trade[0]}: {trade[1]} @ ₹{trade[2]:,.2f} (Qty: {trade[3] if len(trade) > 3 else 'N/A'})")


if __name__ == "__main__":
    main()
