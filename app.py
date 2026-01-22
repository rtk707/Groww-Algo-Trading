from flask import Flask, render_template, jsonify
from config import INITIAL_CAPITAL, DEFAULT_SYMBOL, USE_MOCK_DATA
from data_fetcher import fetch_historical_data
from strategy import calculate_indicators, generate_signals
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

def run_backtest(symbol=None):
    """Run the backtest and return results"""
    if symbol is None:
        symbol = DEFAULT_SYMBOL
    df = fetch_historical_data(symbol, use_mock=USE_MOCK_DATA)
    df = calculate_indicators(df)
    df = generate_signals(df)
    
    final_value, pnl, trades = backtest_strategy(df, INITIAL_CAPITAL)
    
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
    
    # Prepare data for visualization
    chart_data = {
        'timestamps': timestamps_list,
        'close': df['close'].tolist(),
        'sma_20': df['SMA_20'].fillna(0).tolist(),
        'sma_50': df['SMA_50'].fillna(0).tolist(),
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
        'symbol': symbol
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/backtest')
def api_backtest():
    """API endpoint to run backtest"""
    try:
        results = run_backtest()  # Uses DEFAULT_SYMBOL from config
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
