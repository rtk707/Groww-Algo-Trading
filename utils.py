"""
Utility functions for the application
"""
from datetime import datetime


def format_trade_date(trade_date):
    """Format trade date to string consistently"""
    if hasattr(trade_date, 'strftime'):
        return trade_date.strftime('%Y-%m-%d')
    elif isinstance(trade_date, datetime):
        return trade_date.strftime('%Y-%m-%d')
    else:
        return str(trade_date)


def prepare_trade_markers(trades):
    """Prepare buy and sell markers for chart visualization"""
    buy_markers = []
    sell_markers = []
    
    for trade in trades:
        try:
            trade_date_str = format_trade_date(trade[1])
            price = round(trade[2], 2)
            marker = {'x': trade_date_str, 'y': price}
            
            if trade[0] == 'BUY':
                buy_markers.append(marker)
            else:  # SELL
                sell_markers.append(marker)
        except (IndexError, TypeError):
            # Invalid trade format, skip
            continue
    
    return buy_markers, sell_markers


def prepare_chart_data(df, buy_markers, sell_markers):
    """Prepare chart data with strategy-specific indicators"""
    timestamps_list = df['timestamp'].dt.strftime('%Y-%m-%d').tolist()
    
    # Get indicator data with fallback to zeros
    sma_20 = df['SMA_20'].fillna(0).tolist() if 'SMA_20' in df.columns else [0] * len(df)
    sma_50 = df['SMA_50'].fillna(0).tolist() if 'SMA_50' in df.columns else [0] * len(df)
    sma_100 = df['SMA_100'].fillna(0).tolist() if 'SMA_100' in df.columns else None
    sma_200 = df['SMA_200'].fillna(0).tolist() if 'SMA_200' in df.columns else None
    rsi = df['RSI'].fillna(0).tolist() if 'RSI' in df.columns else None
    vwap = df['VWAP'].fillna(0).tolist() if 'VWAP' in df.columns else None
    ema_9 = df['EMA_9'].fillna(0).tolist() if 'EMA_9' in df.columns else None
    ema_20 = df['EMA_20'].fillna(0).tolist() if 'EMA_20' in df.columns else None
    ema_50 = df['EMA_50'].fillna(0).tolist() if 'EMA_50' in df.columns else None
    ema_100 = df['EMA_100'].fillna(0).tolist() if 'EMA_100' in df.columns else None
    ema_200 = df['EMA_200'].fillna(0).tolist() if 'EMA_200' in df.columns else None
    macd = df['MACD'].fillna(0).tolist() if 'MACD' in df.columns else None
    macd_signal = df['MACD_Signal'].fillna(0).tolist() if 'MACD_Signal' in df.columns else None
    macd_histogram = df['MACD_Histogram'].fillna(0).tolist() if 'MACD_Histogram' in df.columns else None
    bb_upper = df['BB_Upper'].fillna(0).tolist() if 'BB_Upper' in df.columns else None
    bb_middle = df['BB_Middle'].fillna(0).tolist() if 'BB_Middle' in df.columns else None
    bb_lower = df['BB_Lower'].fillna(0).tolist() if 'BB_Lower' in df.columns else None
    stoch_k = df['Stoch_K'].fillna(0).tolist() if 'Stoch_K' in df.columns else None
    stoch_d = df['Stoch_D'].fillna(0).tolist() if 'Stoch_D' in df.columns else None
    atr = df['ATR'].fillna(0).tolist() if 'ATR' in df.columns else None
    
    return {
        'timestamps': timestamps_list,
        'close': df['close'].tolist(),
        'sma_20': sma_20,
        'sma_50': sma_50,
        'sma_100': sma_100,
        'sma_200': sma_200,
        'rsi': rsi,
        'vwap': vwap,
        'ema_9': ema_9,
        'ema_20': ema_20,
        'ema_50': ema_50,
        'ema_100': ema_100,
        'ema_200': ema_200,
        'macd': macd,
        'macd_signal': macd_signal,
        'macd_histogram': macd_histogram,
        'bb_upper': bb_upper,
        'bb_middle': bb_middle,
        'bb_lower': bb_lower,
        'stoch_k': stoch_k,
        'stoch_d': stoch_d,
        'atr': atr,
        'signals': df['signal'].tolist(),
        'buy_markers': buy_markers,
        'sell_markers': sell_markers
    }


def format_trades_for_display(trades):
    """Format trades list for frontend display"""
    formatted_trades = []
    for trade in trades:
        date_str = format_trade_date(trade[1])
        formatted_trades.append({
            'action': trade[0],
            'date': date_str,
            'price': round(trade[2], 2),
            'quantity': int(trade[3]) if len(trade) > 3 else 'N/A'
        })
    return formatted_trades

