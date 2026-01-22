def backtest_strategy(df, capital, exit_rules=None, leverage=1, stop_loss_pct=0.10):
    """
    Run backtest with optional leverage and 10% stop-loss (all strategies).

    - leverage: 1, 2, 5, or 10. Buying power = leverage * capital (margin).
      We buy up to `leverage` shares, or fewer if position value would exceed buying power.
    - stop_loss_pct: Exit when position value < this fraction of entry value (default 0.10).
    - exit_rules: Strategy-specific (e.g. RSI +10 / EOD). Stop-loss is checked first.
    """
    cash = capital
    position = 0
    buy_price = None
    buy_index = None
    trades = []
    take_profit = (exit_rules or {}).get("take_profit_rs")
    hold_max_days = (exit_rules or {}).get("hold_max_days")
    use_exit_rules = take_profit is not None and hold_max_days is not None
    leverage = max(1, int(leverage))
    buying_power = leverage * capital

    for i in range(1, len(df)):
        price = df.iloc[i]["close"]
        date = df.iloc[i]["timestamp"]
        pos_signal = df.iloc[i]["position"]

        if pos_signal == 1 and position == 0:
            # Max position value = buying power. Cap qty so qty * price <= buying_power, and qty <= leverage.
            max_qty_by_power = int(buying_power / price) if price > 0 else 0
            qty = min(leverage, max(0, max_qty_by_power))
            if qty < 1:
                continue
            cost = qty * price
            cash -= cost
            position = qty
            buy_price = price
            buy_index = i
            trades.append(("BUY", date, price, qty))

        elif position > 0:
            entry_value = position * buy_price
            current_value = position * price

            # 10% stop-loss (all strategies): exit if traded value < 10% of entry value
            if current_value < stop_loss_pct * entry_value:
                should_sell = True
            elif use_exit_rules:
                should_sell = price >= buy_price + take_profit or (
                    hold_max_days == 1 and i > buy_index
                )
            else:
                should_sell = pos_signal == -1

            if should_sell:
                cash += position * price
                trades.append(("SELL", date, price, position))
                position = 0
                buy_price = None
                buy_index = None

    final_value = cash + position * df.iloc[-1]["close"]
    pnl = final_value - capital
    return final_value, pnl, trades
