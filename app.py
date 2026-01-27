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
from custom_strategy import compute_all_indicators, execute_custom_strategy
from utils import prepare_trade_markers, prepare_chart_data, format_trades_for_display
import socket
import traceback
import json

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

LEVERAGE_MAP = {"1x": 1, "2x": 2, "5x": 5, "10x": 10}
STOP_LOSS_PCT = 0.10


def run_backtest(symbol=None, strategy_id=None, margin=None, custom_strategy=None):
    """Run the backtest and return results. margin: '1x'|'2x'|'5x'|'10x' -> leverage 1|2|5|10."""
    symbol = symbol or DEFAULT_SYMBOL
    leverage = LEVERAGE_MAP.get((margin or "").strip(), 1)

    df = fetch_historical_data(symbol, use_mock=USE_MOCK_DATA)
    
    if custom_strategy:
        # Custom strategy: compute all indicators and execute user conditions
        df = compute_all_indicators(df)
        df = execute_custom_strategy(
            df,
            buy_conditions=custom_strategy.get("buy_conditions", []),
            sell_conditions=custom_strategy.get("sell_conditions", []),
            buy_logic=custom_strategy.get("buy_logic", "AND"),
            sell_logic=custom_strategy.get("sell_logic", "AND")
        )
        exit_rules = None
    else:
        # Predefined strategy
        if strategy_id is None or strategy_id not in STRATEGIES:
            strategy_id = DEFAULT_STRATEGY
        cfg = STRATEGIES[strategy_id]
        calc_fn = getattr(strategy_module, cfg["indicators"])
        signal_fn = getattr(strategy_module, cfg["signals"])
        df = calc_fn(df)
        df = signal_fn(df)
        exit_rules = cfg.get("exit_rules")

    final_value, pnl, trades = backtest_strategy(
        df, INITIAL_CAPITAL, exit_rules=exit_rules, leverage=leverage, stop_loss_pct=STOP_LOSS_PCT
    )
    
    # Prepare data for visualization
    buy_markers, sell_markers = prepare_trade_markers(trades)
    chart_data = prepare_chart_data(df, buy_markers, sell_markers)
    formatted_trades = format_trades_for_display(trades)
    
    return {
        'final_value': round(final_value, 2),
        'pnl': round(pnl, 2),
        'pnl_percent': round((pnl / INITIAL_CAPITAL) * 100, 2),
        'initial_capital': INITIAL_CAPITAL,
        'total_trades': len(trades),
        'trades': formatted_trades,
        'chart_data': chart_data,
        'symbol': symbol,
        'strategy': 'Custom Strategy' if custom_strategy else strategy_id,
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
        is_custom = request.args.get("custom") == "true"
        
        custom_strategy = None
        if is_custom:
            try:
                buy_conditions = json.loads(request.args.get("buy_conditions", "[]"))
                sell_conditions = json.loads(request.args.get("sell_conditions", "[]"))
                custom_strategy = {
                    "buy_conditions": buy_conditions,
                    "sell_conditions": sell_conditions,
                    "buy_logic": request.args.get("buy_logic", "AND"),
                    "sell_logic": request.args.get("sell_logic", "AND")
                }
            except (json.JSONDecodeError, TypeError) as e:
                return jsonify({
                    'error': 'Invalid custom strategy format',
                    'message': str(e)
                }), 400
        
        results = run_backtest(symbol=symbol, strategy_id=strategy_id, margin=margin, custom_strategy=custom_strategy)
        return jsonify(results)
    except ValueError as e:
        print(f"Configuration Error: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'message': 'Please configure your Groww API credentials in .env file'
        }), 400
    except Exception as e:
        print(f"Error in backtest: {traceback.format_exc()}")
        return jsonify({
            'error': str(e),
            'message': 'An unexpected error occurred. Check console for details.'
        }), 500

if __name__ == '__main__':
    port = find_free_port(5000)
    print(f"🌐 Server starting on http://localhost:{port}")
    print(f"📊 Open this URL in your browser to view the dashboard")
    app.run(debug=True, host='0.0.0.0', port=port)
