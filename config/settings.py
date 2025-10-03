# config/settings.py
"""Configuration settings for the arbitrage bot"""

import os

# Environment Detection
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production').lower()

# WebSocket Configuration
WEBSOCKET_URL = "wss://stream.binance.com:9443/stream"
STREAMS = ["btcusdt@bookTicker", "ethusdt@bookTicker"]

# Reconnection Settings
MAX_RECONNECT_ATTEMPTS = 10
INITIAL_RECONNECT_DELAY = 5
MAX_RECONNECT_DELAY = 60

# Connection Health Settings
PING_INTERVAL = 20
PING_TIMEOUT = 10
HEARTBEAT_INTERVAL = 15
STALE_DATA_THRESHOLD = 30000  # 30 seconds in milliseconds

# Display and Monitoring Intervals
DISPLAY_INTERVAL = 10  # Seconds between price displays
CONNECTION_CHECK_INTERVAL = 5  # Seconds between connection checks

# WebSocket Debug Settings
WEBSOCKET_TRACE_ENABLED = ENVIRONMENT == 'development'  # Enable trace in development

# Logging Configuration
LOG_LEVEL = "DEBUG" if ENVIRONMENT == 'development' else "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Trading Pairs (Valid Binance pairs)
TRADING_PAIRS = {
    'BTCUSDT': {'bid': 0, 'ask': 0, 'bid_qty': 0, 'ask_qty': 0, 'timestamp': 0},
    'ETHUSDT': {'bid': 0, 'ask': 0, 'bid_qty': 0, 'ask_qty': 0, 'timestamp': 0}
}
