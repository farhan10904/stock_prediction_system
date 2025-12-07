"""
Configuration file for API keys, symbols, file path, 
sleep time, history period, Fast / Slow MA

"""
from datetime import datetime, timedelta

from secrets import Alpha_Key
api_key = Alpha_Key  # you dont have access to my Key


with open("project/logs/symbols.txt", "r") as file:
    symbols = [line.strip() for line in file]

buy_threshold = 200
sleep_time = 1
history_period = "90d"
interval = "1h"
start_date = (datetime.today() - timedelta(days=729)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")
fixed_data_range = True

analysis_path = "project/data/analysis-{symbol}.csv"
historical_data_path = "project/data/historical_prices-{symbol}.csv"
trade_log_path = "project/data/all_trade_logs.csv"
prices_log_path = "project/data/prices.txt"

run_log_path = "project/logs/run_log.txt"
error_log_path = "project/logs/error_log.txt"
summary_log_path = "project/logs/summary.txt"
profit_summary_csv = "project/logs/profit_summary.csv"
profit_summary_txt = "project/logs/profit_summary.txt"

Fast_MA = "MA10"
Slow_MA = "MA50"

stop_loss = -0.02
take_profit = 0.02

risk_per_trade = 0.05
wallet_balance = 1000

fixed_fee = 0.1
percentage_fee = 0.001
slippage = 0.0005
