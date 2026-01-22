def backtest_strategy(df, capital):
    cash = capital
    position = 0
    trades = []

    for i in range(1, len(df)):
        price = df.iloc[i]["close"]
        date = df.iloc[i]["timestamp"]

        if df.iloc[i]["position"] == 1 and position == 0:
            qty = 1  # Fixed quantity of 1
            if cash >= price:  # Only trade if we have enough cash
                cash -= qty * price
                position = qty
                trades.append(("BUY", date, price, qty))

        elif df.iloc[i]["position"] == -1 and position > 0:
            cash += position * price
            trades.append(("SELL", date, price, position))
            position = 0

    final_value = cash + position * df.iloc[-1]["close"]
    pnl = final_value - capital
    return final_value, pnl, trades
