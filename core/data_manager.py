# core/data_manager.py
"""Data management for price data"""

import threading
import time
from typing import Dict, Any
from ..config.settings import TRADING_PAIRS

class DataManager:
    """Manages price data with thread-safe operations"""
    
    def __init__(self):
        self.price_data = TRADING_PAIRS.copy()
        self.lock = threading.Lock()
    
    def update_price_data(self, symbol: str, bid: float, ask: float, 
                         bid_qty: float, ask_qty: float) -> None:
        """Update price data for a symbol"""
        with self.lock:
            if symbol in self.price_data:
                self.price_data[symbol] = {
                    'bid': bid,
                    'ask': ask,
                    'bid_qty': bid_qty,
                    'ask_qty': ask_qty,
                    'timestamp': int(time.time() * 1000)
                }
    
    def get_price_data(self, symbol: str) -> Dict[str, Any]:
        """Get current price data for a symbol"""
        with self.lock:
            return self.price_data.get(symbol, {})
    
    def get_all_prices(self) -> Dict[str, Dict[str, Any]]:
        """Get all current price data"""
        with self.lock:
            return self.price_data.copy()
    
    def check_data_freshness(self, stale_threshold: int = 30000) -> bool:
        """Check if data is fresh (not stale)"""
        current_time = int(time.time() * 1000)
        with self.lock:
            for symbol, data in self.price_data.items():
                if data['timestamp'] > 0:
                    age = current_time - data['timestamp']
                    if age > stale_threshold:
                        return False
        return True
