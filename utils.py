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
    rsi = df['RSI'].fillna(0).tolist() if 'RSI' in df.columns else None
    vwap = df['VWAP'].fillna(0).tolist() if 'VWAP' in df.columns else None
    ema_9 = df['EMA_9'].fillna(0).tolist() if 'EMA_9' in df.columns else None
    ema_20 = df['EMA_20'].fillna(0).tolist() if 'EMA_20' in df.columns else None
    
    return {
        'timestamps': timestamps_list,
        'close': df['close'].tolist(),
        'sma_20': sma_20,
        'sma_50': sma_50,
        'rsi': rsi,
        'vwap': vwap,
        'ema_9': ema_9,
        'ema_20': ema_20,
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

