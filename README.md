# stock_prediction_system

# 📈 Stock Prediction System

A modular Python-based stock prediction and backtesting system designed to fetch real-time and historical data, generate technical indicators, and simulate automated trading behaviour. The system is structured into reusable modules, making it easy to extend, debug, and integrate with future machine learning models.

---

## 🔧 Features

- Modular architecture (fetcher, indicators, strategy, backtester, config)
- Fetches real-time & historical data using YFinance
- Hourly data fetching with caching and structured folders
- Moving averages (MA2–MA50) and trend-based signals
- Custom backtesting engine with:
  - Buy/sell logic
  - Stop-loss / take-profit
  - Trade logging
- Ready for ML integration (future module planned)

---

## 📂 Project Structure

modules/
fetcher.py # Data fetching (YFinance)
indicators.py # Moving averages, trend detection
strategy.py # Buy/sell rules
backtester.py # Simulation engine
config.py # Settings (tickers, timeframes)
utils.py # Helpers

data/
Hourly/ # Cached hourly data
Daily/ # Daily data

main.py # Runs the full pipeline
