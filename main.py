# main.py
"""Main application entry point"""

import time
import threading
from .utils.logger import setup_logger
from .core.data_manager import DataManager
from .core.websocket_client import BinanceWebSocketClient

def main():
    """Main function"""
    logger = setup_logger(__name__)
    logger.info("Starting Binance Arbitrage Bot...")
    
    # Initialize components
    data_manager = DataManager()
    ws_client = BinanceWebSocketClient(data_manager)
    
    try:
        # Start WebSocket in a separate thread
        ws_thread = threading.Thread(target=ws_client.start, daemon=True)
        ws_thread.start()
        
        # Start heartbeat monitor in a separate thread
        heartbeat_thread = threading.Thread(target=ws_client.start_heartbeat_monitor, daemon=True)
        heartbeat_thread.start()
        
        # Keep the main thread alive and show status
        while True:
            if ws_client.is_connected():
                # Display current prices every 10 seconds
                time.sleep(10)
                prices = data_manager.get_all_prices()
                logger.info("=== Current Price Data ===")
                for symbol, data in prices.items():
                    if data['bid'] > 0 and data['ask'] > 0:
                        spread = data['ask'] - data['bid']
                        spread_pct = (spread / data['bid']) * 100
                        logger.info(f"{symbol}: Bid=${data['bid']:.4f}, Ask=${data['ask']:.4f}, Spread={spread_pct:.3f}%")
                logger.info("=========================")
            else:
                logger.warning("WebSocket not connected. Waiting...")
                time.sleep(5)
                
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        ws_client.stop()

if __name__ == "__main__":
    main()