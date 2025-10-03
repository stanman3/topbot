# main.py
"""Main application entry point"""

import asyncio
import time
import threading
from .utils.logger import setup_logger
from .core.data_manager import DataManager
from .core.websocket_client import BinanceWebSocketClient
from .config.settings import DISPLAY_INTERVAL, CONNECTION_CHECK_INTERVAL

async def display_prices(data_manager, logger):
    """Display current prices asynchronously"""
    logger.info("Display prices task started")
    try:
        while True:
            prices = data_manager.get_all_prices()
            logger.info("=== Current Price Data ===")
            for symbol, data in prices.items():
                if data['bid'] > 0 and data['ask'] > 0:
                    spread = data['ask'] - data['bid']
                    spread_pct = (spread / data['bid']) * 100
                    logger.info(f"{symbol}: Bid=${data['bid']:.4f}, Ask=${data['ask']:.4f}, Spread={spread_pct:.3f}%")
            logger.info("=========================")
            
            # Use configurable interval
            await asyncio.sleep(DISPLAY_INTERVAL)
            
    except asyncio.CancelledError:
        logger.info("display_prices task cancelled")
    except Exception as e:
        logger.error(f"Error in display_prices: {e}")
    finally:
        logger.info("display_prices task stopped")

async def connection_monitor(ws_client, logger):
    """Monitor connection status asynchronously"""
    logger.info("Connection monitor task started")
    try:
        while True:
            if not ws_client.is_connected():
                logger.warning("WebSocket not connected. Waiting...")
            await asyncio.sleep(CONNECTION_CHECK_INTERVAL)
    except asyncio.CancelledError:
        logger.info("connection_monitor task cancelled")
    except Exception as e:
        logger.error(f"Error in connection_monitor: {e}")
    finally:
        logger.info("connection_monitor task stopped")

async def main_async():
    """Main async function"""
    logger = setup_logger(__name__)
    logger.info("Starting Binance Arbitrage Bot...")
    
    # Initialize components
    data_manager = DataManager()
    ws_client = BinanceWebSocketClient(data_manager)
    
    # Start WebSocket in thread pool without blocking event loop
    loop = asyncio.get_event_loop()
    # Wrap in lambda to catch any exceptions from start()
    loop.run_in_executor(None, lambda: ws_client.start())
    
    # Note: heartbeat monitor will be started as an async task
    
    # Wait a moment for connection to establish
    await asyncio.sleep(2)
    
    # Run async tasks concurrently with proper cancellation handling
    tasks = [
        asyncio.create_task(display_prices(data_manager, logger)),
        asyncio.create_task(connection_monitor(ws_client, logger)),
        asyncio.create_task(ws_client.start_heartbeat_monitor())
    ]
    
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        logger.info("Main tasks cancelled, shutting down...")
        # Cancel all tasks gracefully
        for task in tasks:
            if not task.done():
                task.cancel()
        # Wait for tasks to complete cancellation
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        ws_client.shutdown()

def main():
    """Main function - entry point"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()