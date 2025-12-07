"""
Utility functions for logging, saving prices, 
and loading price logs into a DataFrame.
"""

import pandas as pd
from datetime import datetime
from config import error_log_path, prices_log_path

def log_error(symbol,error):
     """
     Logs an error message with a timestamp 
     to the error log file.
     """

     with open(error_log_path, "a") as file:
            file.write(f"[{datetime.now()}] API call failed for {symbol}: {error}\n")

def save_price(symbol, price):
      """
      Appends the current price
      of a symbol to the prices log file.
      """
     
      with open(prices_log_path, "a") as file:
        file.write(f"[{datetime.now()}] {symbol} price: {price} \n")

def load_prices(filepath):
      """
      Parses a price log file into a DataFrame with Timestamp
      Symbol and Price columns.

      """       
      prices = []
      symbols = []
      time_stamps = []

      with open(filepath, "r") as file:
          for line in file:
               try: 
                    parts = line.split("]")
               
                    time_stamps.append(parts[0].replace("[", "").strip())
               
                    rest_line = parts[1]
                    part = rest_line.split("price:")
               
                    symbols.append(part[0].strip())
               
                    prices.append(float(part[1]))
               
               except Exception as e:
                    log_error("load_Prices", 
                         f"Malformed line: {line.strip()} — {e}")
         
      DF = {
         "Timestamp": time_stamps,  
         "Symbol": symbols,
         "Price": prices
         }
     
      df = pd.DataFrame(DF)
      return(df)

     




