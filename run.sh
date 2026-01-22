#!/bin/bash

# Groww Algo Trading - Run Script
# This script starts both the backend (Flask) and serves the frontend

echo "🚀 Starting Groww Algo Trading Application..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start the Flask server
echo ""
echo "✅ Starting Flask server..."
echo "🌐 The server will automatically find an available port"
echo "📊 Look for the URL in the output above, then click 'Start Backtest'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
