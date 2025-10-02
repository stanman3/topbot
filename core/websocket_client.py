# core/websocket_client.py
"""Binance WebSocket client for real-time data"""

import websocket
import json
import threading
import time
from typing import Callable
from ..utils.logger import get_logger
from .data_manager import DataManager
from ..config.settings import (
    WEBSOCKET_URL, STREAMS, MAX_RECONNECT_ATTEMPTS, 
    INITIAL_RECONNECT_DELAY, MAX_RECONNECT_DELAY,
    PING_INTERVAL, PING_TIMEOUT, HEARTBEAT_INTERVAL,
    STALE_DATA_THRESHOLD
)

logger = get_logger(__name__)

class BinanceWebSocketClient:
    """Robust WebSocket client for Binance data streams"""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ws = None
        self.is_running = False
        self.reconnect_attempts = 0
        self.reconnect_delay = INITIAL_RECONNECT_DELAY
        self.heartbeat_thread = None
        
    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            if 'stream' in data and 'data' in data:
                stream = data['stream']
                ticker_data = data['data']
                
                if 'bookTicker' in stream:
                    symbol = ticker_data['s']
                    bid = float(ticker_data['b'])
                    bid_qty = float(ticker_data['B'])
                    ask = float(ticker_data['a'])
                    ask_qty = float(ticker_data['A'])
                    
                    # Update data manager
                    self.data_manager.update_price_data(
                        symbol, bid, ask, bid_qty, ask_qty
                    )
                    
                    logger.info(f"{symbol}: Bid=${bid:.4f} (Qty: {bid_qty:.2f}), Ask=${ask:.4f} (Qty: {ask_qty:.2f})")
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        logger.error(f"WebSocket error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        logger.warning(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.is_running = False
        
        # Attempt to reconnect
        if self.reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
            self.reconnect_attempts += 1
            logger.info(f"Attempting to reconnect... ({self.reconnect_attempts}/{MAX_RECONNECT_ATTEMPTS})")
            self.reconnect_delay = min(MAX_RECONNECT_DELAY, self.reconnect_delay * 2)
            time.sleep(self.reconnect_delay)
            self.start()
        else:
            logger.error("Max reconnection attempts reached. Stopping.")
    
    def on_open(self, ws):
        """Handle WebSocket open"""
        logger.info("WebSocket connection established")
        self.reconnect_attempts = 0
        self.reconnect_delay = INITIAL_RECONNECT_DELAY
        logger.info(f"Subscribed to streams: {', '.join(STREAMS)}")
    
    def start_heartbeat_monitor(self):
        """Monitor connection health"""
        while self.is_running:
            time.sleep(HEARTBEAT_INTERVAL)
            if not self.data_manager.check_data_freshness(STALE_DATA_THRESHOLD):
                logger.warning("Connection health check failed - data is stale")
    
    def start(self):
        """Start the WebSocket connection"""
        if self.is_running:
            return
            
        self.is_running = True
        websocket.enableTrace(False)
        
        # Build WebSocket URL with streams
        streams_param = "/".join(STREAMS)
        ws_url = f"{WEBSOCKET_URL}?streams={streams_param}"
        
        try:
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )
            
            logger.info("Starting WebSocket connection...")
            self.ws.run_forever(ping_interval=PING_INTERVAL, ping_timeout=PING_TIMEOUT)
            
        except Exception as e:
            logger.error(f"Failed to start WebSocket: {e}")
            self.is_running = False
    
    def stop(self):
        """Stop the WebSocket connection"""
        self.is_running = False
        if self.ws:
            self.ws.close()
        logger.info("WebSocket connection stopped")
    
    def is_connected(self):
        """Check if WebSocket is connected"""
        return self.is_running and self.ws is not None
