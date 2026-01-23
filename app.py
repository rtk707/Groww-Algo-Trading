from flask import Flask, render_template, jsonify, request
from config import (
    INITIAL_CAPITAL,
    DEFAULT_SYMBOL,
    USE_MOCK_DATA,
    STRATEGIES,
    DEFAULT_STRATEGY,
    AVAILABLE_STOCKS,
)
from data_fetcher import fetch_historical_data
import strategy as strategy_module
from backtest import backtest_strategy
import json
import socket
import requests
from datetime import datetime

app = Flask(__name__)

def find_free_port(start_port=5000, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")

def run_backtest(symbol=None, strategy_id=None, margin=None):
    """Run the backtest and return results. margin: '2x'|'5x'|'10x' -> leverage 2|5|10."""
    if symbol is None:
        symbol = DEFAULT_SYMBOL
    if strategy_id is None or strategy_id not in STRATEGIES:
        strategy_id = DEFAULT_STRATEGY
    cfg = STRATEGIES[strategy_id]
    calc_fn = getattr(strategy_module, cfg["indicators"])
    signal_fn = getattr(strategy_module, cfg["signals"])

    leverage_map = {"2x": 2, "5x": 5, "10x": 10}
    leverage = leverage_map.get((margin or "").strip(), 2)

    df = fetch_historical_data(symbol, use_mock=USE_MOCK_DATA)
    df = calc_fn(df)
    df = signal_fn(df)

    exit_rules = cfg.get("exit_rules")
    final_value, pnl, trades = backtest_strategy(
        df, INITIAL_CAPITAL, exit_rules=exit_rules, leverage=leverage, stop_loss_pct=0.10
    )
    
    # Prepare trade markers for chart
    buy_markers = []
    sell_markers = []
    timestamps_list = df['timestamp'].dt.strftime('%Y-%m-%d').tolist()
    
    for trade in trades:
        # Handle different timestamp formats
        trade_date = trade[1]
        if hasattr(trade_date, 'strftime'):
            trade_date_str = trade_date.strftime('%Y-%m-%d')
        elif isinstance(trade_date, datetime):
            trade_date_str = trade_date.strftime('%Y-%m-%d')
        else:
            trade_date_str = str(trade_date)
        
        # Find matching timestamp index
        try:
            timestamp_idx = timestamps_list.index(trade_date_str)
            price = round(trade[2], 2)
            
            if trade[0] == 'BUY':
                buy_markers.append({
                    'x': trade_date_str,
                    'y': price
                })
            else:  # SELL
                sell_markers.append({
                    'x': trade_date_str,
                    'y': price
                })
        except ValueError:
            # Date not found in timestamps, skip
            pass
    
    # Prepare data for visualization (strategy-specific indicators)
    sma_20 = df['SMA_20'].fillna(0).tolist() if 'SMA_20' in df.columns else [0] * len(df)
    sma_50 = df['SMA_50'].fillna(0).tolist() if 'SMA_50' in df.columns else [0] * len(df)
    rsi = df['RSI'].fillna(0).tolist() if 'RSI' in df.columns else None
    vwap = df['VWAP'].fillna(0).tolist() if 'VWAP' in df.columns else None
    ema_9 = df['EMA_9'].fillna(0).tolist() if 'EMA_9' in df.columns else None
    ema_20 = df['EMA_20'].fillna(0).tolist() if 'EMA_20' in df.columns else None
    chart_data = {
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
    
    # Format trades for display
    formatted_trades = []
    for trade in trades:
        # Handle different timestamp formats
        date_str = trade[1]
        if hasattr(date_str, 'strftime'):
            date_str = date_str.strftime('%Y-%m-%d')
        elif isinstance(date_str, datetime):
            date_str = date_str.strftime('%Y-%m-%d')
        else:
            date_str = str(date_str)
        
        formatted_trades.append({
            'action': trade[0],
            'date': date_str,
            'price': round(trade[2], 2),
            'quantity': int(trade[3]) if len(trade) > 3 else 'N/A'
        })
    
    return {
        'final_value': round(final_value, 2),
        'pnl': round(pnl, 2),
        'pnl_percent': round((pnl / INITIAL_CAPITAL) * 100, 2),
        'initial_capital': INITIAL_CAPITAL,
        'total_trades': len(trades),
        'trades': formatted_trades,
        'chart_data': chart_data,
        'symbol': symbol,
        'strategy': strategy_id,
        'margin': f"{leverage}x",
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/strategies')
def api_strategies():
    """Return list of strategy names for dropdown"""
    strategies = [{"id": name, "name": name} for name in STRATEGIES]
    return jsonify({"strategies": strategies, "default": DEFAULT_STRATEGY})


@app.route('/api/stocks')
def api_stocks():
    """Return list of available stocks for dropdown"""
    return jsonify({"stocks": AVAILABLE_STOCKS, "default": DEFAULT_SYMBOL})


@app.route('/api/backtest')
def api_backtest():
    """API endpoint to run backtest"""
    try:
        strategy_id = request.args.get("strategy")
        margin = request.args.get("margin")
        symbol = request.args.get("symbol")
        results = run_backtest(symbol=symbol, strategy_id=strategy_id, margin=margin)
        return jsonify(results)
    except ValueError as e:
        # Configuration or data format errors
        import traceback
        error_details = traceback.format_exc()
        print(f"Configuration Error: {error_details}")
        return jsonify({
            'error': str(e),
            'message': 'Please configure your Groww API credentials in config.py'
        }), 400
    except requests.exceptions.RequestException as e:
        # API request errors
        import traceback
        error_details = traceback.format_exc()
        print(f"API Request Error: {error_details}")
        return jsonify({
            'error': str(e),
            'message': 'Failed to fetch data from Groww API. Check your credentials and network connection.'
        }), 500
    except Exception as e:
        # Other errors
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in backtest: {error_details}")
        return jsonify({
            'error': str(e),
            'message': 'An unexpected error occurred. Check console for details.'
        }), 500

if __name__ == '__main__':
    port = find_free_port(5000)
    print(f"🌐 Server starting on http://localhost:{port}")
    print(f"📊 Open this URL in your browser to view the dashboard")
    app.run(debug=True, host='0.0.0.0', port=port)
