# Crypto Arbitrage Trading Bot 🚀

A robust, real-time cryptocurrency arbitrage bot that monitors Binance WebSocket streams for trading opportunities between BTC/USDT and ETH/USDT pairs.

### Trading Pairs Monitored
- **BTC/USDT** - Bitcoin to USDT
- **ETH/USDT** - Ethereum to USDT

## 📂 Repository Structure
```
topbot/
├── __init__.py                 # Package initialization
├── main.py                     # Main application entry point
├── README.md                   # This file
├── config/                     # Configuration settings
│   ├── __init__.py
│   └── settings.py            # All configuration parameters
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── websocket_client.py    # WebSocket client implementation
│   └── data_manager.py        # Data management and storage
└── utils/                      # Utility functions
    ├── __init__.py
    └── logger.py              # Logging configuration
```

## 🔧 Configuration
All configuration settings are centralized in `config/settings.py`:

The bot supports different configurations based on the `ENVIRONMENT` variable:

**Development Mode:**
```bash
# Enable WebSocket tracing and debug logging
set ENVIRONMENT=development
py -m topbot.main
```

**Production Mode (default):**
```bash
# Disable tracing, use INFO logging
py -m topbot.main
```

**Environment Variables:**
- `ENVIRONMENT=development` - Enables WebSocket tracing and DEBUG logging
- `ENVIRONMENT=production` - Disables tracing, uses INFO logging (default)

### Monitoring Output
```
2024-01-10 15:30:45 - INFO - BTCUSDT: Bid=$45,230.50 (Qty: 0.15), Ask=$45,231.00 (Qty: 0.20)
2024-01-10 15:30:45 - INFO - ETHUSDT: Bid=$2,650.25 (Qty: 1.50), Ask=$2,650.75 (Qty: 2.30)
2024-01-10 15:30:50 - INFO - === Current Price Data ===
2024-01-10 15:30:50 - INFO - BTCUSDT: Bid=$45,230.50, Ask=$45,231.00, Spread=0.001%
2024-01-10 15:30:50 - INFO - ETHUSDT: Bid=$2,650.25, Ask=$2,650.75, Spread=0.019%
```

### Installation Steps

1. **Install required packages:**
   ```bash
   pip install websocket-client ccxt python-binance pandas numpy python-dotenv
   ```

2. **Run the application:**
   ```bash
   # From the parent directory
   py -m topbot.main
   
   # Or from within the topbot directory
   cd topbot
   py main.py
   ```