def backtest_strategy(df, capital, exit_rules=None, leverage=1, stop_loss_pct=0.10):
    """
    Run backtest with optional leverage and stop-loss.
    
    Args:
        df: DataFrame with 'close', 'timestamp', 'position' columns
        capital: Initial capital
        exit_rules: Dict with 'take_profit_rs' and 'hold_max_days' (optional)
        leverage: 1, 2, 5, or 10. Buying power = leverage * capital
        stop_loss_pct: Exit when position value < this fraction of entry value
    
    Returns:
        tuple: (final_value, pnl, trades)
    """
    cash = capital
    position = 0
    buy_price = None
    buy_index = None
    trades = []
    
    exit_rules = exit_rules or {}
    take_profit = exit_rules.get("take_profit_rs")
    hold_max_days = exit_rules.get("hold_max_days")
    use_exit_rules = take_profit is not None and hold_max_days is not None
    
    leverage = max(1, int(leverage))
    buying_power = leverage * capital

    for i in range(1, len(df)):
        price = df.iloc[i]["close"]
        date = df.iloc[i]["timestamp"]
        pos_signal = df.iloc[i]["position"]

        # Buy signal
        if pos_signal == 1 and position == 0:
            max_qty_by_power = int(buying_power / price) if price > 0 else 0
            qty = min(leverage, max(0, max_qty_by_power))
            if qty < 1:
                continue
            
            cash -= qty * price
            position = qty
            buy_price = price
            buy_index = i
            trades.append(("BUY", date, price, qty))

        # Sell logic
        elif position > 0:
            entry_value = position * buy_price
            current_value = position * price
            should_sell = False

            # Stop-loss check (priority)
            if current_value < stop_loss_pct * entry_value:
                should_sell = True
            # Strategy-specific exit rules
            elif use_exit_rules:
                should_sell = (price >= buy_price + take_profit or 
                              (hold_max_days == 1 and i > buy_index))
            # Default: sell on strategy signal
            else:
                should_sell = pos_signal == -1

            if should_sell:
                cash += position * price
                trades.append(("SELL", date, price, position))
                position = 0
                buy_price = None
                buy_index = None

    final_value = cash + (position * df.iloc[-1]["close"] if position > 0 else 0)
    return final_value, final_value - capital, trades
