# Crypto Arbitrage Trading Bot 🚀

A robust, real-time cryptocurrency arbitrage bot that monitors Binance WebSocket streams for trading opportunities between BTC/USDT and ETH/USDT pairs.

## ⚙️ Tech Stack
- **Language:** Python 3.8+
- **APIs:** Binance WebSocket API
- **Libraries:** 
  - `websocket-client` - WebSocket connections
  - `ccxt` - Cryptocurrency exchange library
  - `python-binance` - Binance API client
  - `pandas` - Data manipulation
  - `numpy` - Numerical calculations

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

- **WebSocket settings** - Connection URLs and streams
- **Reconnection settings** - Retry attempts and delays
- **Trading pairs** - Monitored cryptocurrency pairs
- **Logging settings** - Log levels and formats

## 📊 Usage

### Basic Usage
The bot automatically:
1. Connects to Binance WebSocket streams
2. Monitors BTC/USDT and ETH/USDT price data
3. Displays real-time bid/ask prices and spreads
4. Handles connection issues with automatic reconnection

### Monitoring Output
```
2024-01-10 15:30:45 - INFO - BTCUSDT: Bid=$45,230.50 (Qty: 0.15), Ask=$45,231.00 (Qty: 0.20)
2024-01-10 15:30:45 - INFO - ETHUSDT: Bid=$2,650.25 (Qty: 1.50), Ask=$2,650.75 (Qty: 2.30)
2024-01-10 15:30:50 - INFO - === Current Price Data ===
2024-01-10 15:30:50 - INFO - BTCUSDT: Bid=$45,230.50, Ask=$45,231.00, Spread=0.001%
2024-01-10 15:30:50 - INFO - ETHUSDT: Bid=$2,650.25, Ask=$2,650.75, Spread=0.019%
```

## 🚀 Features

- ✅ **Real-time WebSocket data streaming** from Binance
- ✅ **Robust connection management** with automatic reconnection
- ✅ **Thread-safe data handling** with proper locking mechanisms
- ✅ **Connection health monitoring** with stale data detection
- ✅ **Modular architecture** for easy maintenance and expansion
- ✅ **Comprehensive logging** for debugging and monitoring

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

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