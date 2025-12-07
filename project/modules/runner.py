"""
Orchestrates all major stock predictor project operations:
- Running live predictions and logging signals
- Preparing analysis features and signals
- Performing backtests and exporting trade logs
- Fetching historical price data for all symbols
- Summarizing profit/loss statistics

This module acts as the main control center, 
calling all pipeline steps and saving results/logs to file.

"""

from modules.indicators import add_ma, add_percent_change, add_trend
from modules.strategy import generate_signals, add_position
from config import symbols, buy_threshold, sleep_time, wallet_balance, interval
from modules.backtest import backtest_signals
from modules.price_fetcher import get_price, get_historical_data
from modules.utils import save_price
from config import (analysis_path, run_log_path, 
historical_data_path, trade_log_path, profit_summary_csv, profit_summary_txt)
from datetime import datetime

import pandas as pd
import time
import os

def run_backtests():
    """
    Runs backtests on all analyzed symbols.
    
    Prints summary stats for each symbol 
    (trades, win rate, P&L).

    """
    
    symbol_trade_count = {}

    for symbol in symbols:
        per_stock_balance = wallet_balance / len(symbols)
        
        df = pd.read_csv(analysis_path.format(symbol = symbol))
        #print(df[["Timestamp", "Signal", "Position"]].head(30))
        
        print(f"Backtest for {symbol}:")
        results, trade_log = backtest_signals(df, balance = per_stock_balance) 
        print(f"Total Trades: {results['Total Trades']}")
        print(f"Win Rate: {results['Win Rate']:.2f}%")
        print(f"Wins:{results['Wins']}")
        print(f"Average Win: {results['Average Win']:.2f}")
        print(f"Losses: {results['Losses']}")
        print(f"Average Loss: {results['Average Loss']:.2f}")
        print(f"Expectancy: {results['expectancy']}")
        print(f"Long Trades: {results['Long Trades']}")
        print(f"Short Trades: {results['Short Trades']}")
        print(f"Total Profit: £{results['Total Profit']:.2f}\n")
        df_trade_log = pd.DataFrame(trade_log)
        df_trade_log.to_csv(f"project/logs/trade_{symbol}.csv", index = False)
        symbol_trade_count[symbol] = results['Total Trades']
        print()

def run_predictor():
     """
     Runs the live stock predictor loop.
     Fetches latest prices, 
     
     prints/saves buy signals, and logs run summary.
     
     """
     
     start_time = datetime.now()
     
     with open(run_log_path, "a") as file:
         file.write(f"[{datetime.now()}] Stock predictor run started. \n")
     
     buy_signal = 0

     for symbol in symbols:
    
        price = get_price(symbol)

        if price is None:
            continue

        if float(price) >buy_threshold:
            print(f"Buy signal for {symbol}! Price: {price}")
            buy_signal += 1
        else:
            print(f"No buy signal for {symbol}. Price: {price}")
    
        save_price(symbol, price)

        time.sleep(sleep_time)

     print(f"Run complete. {len(symbols)} symbols processed. {buy_signal} buy signals")

     with open(run_log_path, "a") as file:
         file.write(f"[{datetime.now()}] Run complete. {len(symbols)} symbols processed. {buy_signal} buy signals \n")

     end_time = datetime.now()

     duration = end_time - start_time
     with open(run_log_path, "a") as file:
         file.write(f"Run duration: {duration.total_seconds()} seconds \n")
     
     with open(run_log_path, "a") as file:
         file.write(f"[{datetime.now()}] Run complete. {len(symbols)} symbols processed. {buy_signal} buy signals. Run duration: {duration.total_seconds()} seconds \n ")

def prepare_analysis():
    """
    Prepares analysis data for each symbol.
    Loads historical data, 
    
    adds technical features/signals, and saves results.
    
    """
    folder = "Hourly" if interval == "1h" else "Daily"
    analysis_folder = "Analysis_Hourly" if interval == "1h" else "Analysis_Daily"

    for symbol in symbols:
       
        # Load historical data from correct folder
       
        hist_path = f"project/data/{folder}/historical_prices-{symbol}.csv"
        df_symbol = pd.read_csv(hist_path)

        # Rename Datetime to Timestamp if it exists
        if "Datetime" in df_symbol.columns:
            df_symbol = df_symbol.rename(columns={"Datetime": "Timestamp"})

        # Ensure Timestamp is datetime type
        if not pd.api.types.is_datetime64_any_dtype(df_symbol["Timestamp"]):
            df_symbol["Timestamp"] = pd.to_datetime(df_symbol["Timestamp"])

        df_symbol = df_symbol.reset_index(drop=True)
    
        # Add indicators and signals
        df_symbol = add_ma(df_symbol, 10)
        df_symbol = add_ma(df_symbol, 50)
        df_symbol = add_percent_change(df_symbol)
        df_symbol = add_trend(df_symbol, "MA50")
        df_symbol = generate_signals(df_symbol)
        df_symbol = add_position(df_symbol)

        # Save to correct analysis folder

        output_path = f"project/data/{analysis_folder}/analysis-{symbol}.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_symbol.to_csv(output_path, index=False)

        #print(df_symbol[["Timestamp","MA10","MA50", "Signal", "Position"]].iloc[45:70])
        print(f"Analysis saved for {symbol}")
        
def export_all_trades():
    """
    Exports the full trade log 
    for all symbols to a single CSV.
    
    Creates trade logs from each symbol 
    for easy project tracking.
    """

    all_trade = []
    for symbol in symbols:

        per_stock_balance = wallet_balance / len(symbols)

        df = pd.read_csv(analysis_path.format(symbol = symbol))
        results, trade_log = backtest_signals(df, balance = per_stock_balance)
        all_trade.extend(trade_log)
    df_all_trade = pd.DataFrame(all_trade)
    df_all_trade.to_csv(trade_log_path, index = False)

def get_all_historical_data():
    """
    Fetches and saves historical price data for all symbols 
    in the project.
    
    Uses yfinance or similar for bulk data collection.
    
    """
    
    for symbol in symbols:
         get_historical_data(symbol)

def profit_summary():

    """
    Calculates and logs profit/loss statistics 
    based on all trades.

    Outputs total profit, win rate, average win/loss, 
    and max wins/losses to log files.
    
    """

    header = not os.path.exists(profit_summary_csv)

    df = pd.read_csv(trade_log_path)
    total_profit = df["Profit"].sum()
    win_rate = (df["Profit"] > 0).mean() * 100
    avg_win = df[df["Profit"] > 0]["Profit"].mean()
    avg_loss = df[df["Profit"] < 0]["Profit"].mean()
    max_win = df["Profit"].max()
    max_loss = df["Profit"].min()
    
    with open(profit_summary_txt, "a") as file:
        file.write(f"[{datetime.now()}]\n")
        file.write(f"Total Profit: £{total_profit:.2f}\n")
        file.write(f"Win Rate: {win_rate:.2f}%\n")
        file.write(f"Average Win: £{avg_win:.2f}\n")
        file.write(f"Average Loss: £{avg_loss:.2f}\n")
        file.write(f"Biggest Win: £{max_win:.2f}\n")
        file.write(f"Biggest Loss: £{max_loss:.2f}\n")
        file.write("-" * 35 + "\n")
    
    df_summary = pd.DataFrame([{
        "Date": datetime.now(), 
        "Total Profit": total_profit,
        "Win Rate": win_rate,
        "Average Win": avg_win,
        "Average Loss": avg_loss,
        "Biggest Win": max_win,
        "Biggest Loss": max_loss }])
    
    df_summary.to_csv(profit_summary_csv, 
        mode = "a", header = header, index = False)