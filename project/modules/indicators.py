"""
Technical indicators: moving averages, 
percent change, and trend detection based on price data.
"""

import pandas as pd
import numpy as np

def add_ma(df, window):
    """
    Adds a moving average column (MA{window}) to the 
    DataFrame based on 'Price'.
    """
    
    df[f"MA{window}"] = df["Price"].rolling(window=window).mean()
    
    return df

def add_percent_change(df):
    """
    Calculates and adds percentage price change between rows.
    """
    df["Percentage_Change"] =  df["Price"].pct_change()*100
    
    return df

def add_trend(df, column_name):
    """
    Adds a trend column showing +1 (up), -1 (down), or 0 
    for flat, based on a given column.
    """

    diff = np.diff(df[column_name])
    
    trend = np.sign(diff)
    
    df[f"{column_name}_trend"] = [np.nan] + list(trend)
    
    return df

