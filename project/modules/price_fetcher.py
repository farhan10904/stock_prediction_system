"""
Fetches real-time and historical stock prices 
using Alpha Vantage and yfinance.

"""

import requests
import yfinance as yf
import pandas as pd
import os


from config import api_key, history_period, historical_data_path, interval, start_date, end_date, fixed_data_range
from modules.utils import log_error

def get_price(symbol):
    """
    pulls real-time prices form Alpha Vantage
    returns a price string or None if request fails
    logs error using lof_error()
    
    """
    
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = data["Global Quote"]["05. price"]
        return price
    except Exception as e:
         log_error(symbol, e)
         print(f"API call failed for {symbol}: {e}")
         return None
    
def get_historical_data(symbol):

    """
    Uses yfinance
    saves a CSV file to data folder
    uses error handling if download fails
    
    """
    try:
        if fixed_data_range:
            df = yf.download(symbol, start = start_date, end = end_date, 
                            interval = interval,
                            auto_adjust=True, progress = False,)
        else:
            df = yf.download(symbol, period = history_period, 
                            interval = interval,
                            auto_adjust=True, progress = False,)

       
        if df is None or df.empty:
            log_error("Get_Historical_Data", f"{symbol} - No data returned")
            return
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
    
        df["Symbol"] = symbol
        df["Price"] = df["Close"]
        df = df.reset_index()
        df = df.rename(columns={"Date": "Timestamp"})
        
        #interval determines save folder

        folder = "Hourly" if interval == "1h" else "Daily"
        path = historical_data_path.format(symbol = symbol).replace("project/data/", f"project/data/{folder}/")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, 
                  index = False)
    
    except Exception as e:
        log_error("Get_Historical_Data", f"{symbol} - {e}")



 