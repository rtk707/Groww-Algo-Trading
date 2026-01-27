"""
Utility functions for the application
"""
from datetime import datetime


def format_trade_date(trade_date):
    """Format trade date to string consistently"""
    if isinstance(trade_date, datetime) or hasattr(trade_date, 'strftime'):
        return trade_date.strftime('%Y-%m-%d')
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


def _get_indicator_list(df, column_name):
    """Helper to get indicator list or None if column doesn't exist"""
    if column_name in df.columns:
        return df[column_name].fillna(0).tolist()
    return None


def prepare_chart_data(df, buy_markers, sell_markers):
    """Prepare chart data with strategy-specific indicators"""
    return {
        'timestamps': df['timestamp'].dt.strftime('%Y-%m-%d').tolist(),
        'close': df['close'].tolist(),
        'sma_20': _get_indicator_list(df, 'SMA_20') or [0] * len(df),
        'sma_50': _get_indicator_list(df, 'SMA_50') or [0] * len(df),
        'sma_100': _get_indicator_list(df, 'SMA_100'),
        'sma_200': _get_indicator_list(df, 'SMA_200'),
        'rsi': _get_indicator_list(df, 'RSI'),
        'vwap': _get_indicator_list(df, 'VWAP'),
        'ema_9': _get_indicator_list(df, 'EMA_9'),
        'ema_20': _get_indicator_list(df, 'EMA_20'),
        'ema_50': _get_indicator_list(df, 'EMA_50'),
        'ema_100': _get_indicator_list(df, 'EMA_100'),
        'ema_200': _get_indicator_list(df, 'EMA_200'),
        'macd': _get_indicator_list(df, 'MACD'),
        'macd_signal': _get_indicator_list(df, 'MACD_Signal'),
        'macd_histogram': _get_indicator_list(df, 'MACD_Histogram'),
        'bb_upper': _get_indicator_list(df, 'BB_Upper'),
        'bb_middle': _get_indicator_list(df, 'BB_Middle'),
        'bb_lower': _get_indicator_list(df, 'BB_Lower'),
        'stoch_k': _get_indicator_list(df, 'Stoch_K'),
        'stoch_d': _get_indicator_list(df, 'Stoch_D'),
        'atr': _get_indicator_list(df, 'ATR'),
        'signals': df['signal'].tolist(),
        'buy_markers': buy_markers,
        'sell_markers': sell_markers
    }


def format_trades_for_display(trades):
    """Format trades list for frontend display"""
    return [
        {
            'action': trade[0],
            'date': format_trade_date(trade[1]),
            'price': round(trade[2], 2),
            'quantity': int(trade[3]) if len(trade) > 3 else 'N/A'
        }
        for trade in trades
    ]

