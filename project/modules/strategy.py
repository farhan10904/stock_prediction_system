"""
Trading strategy logic for generating signals 
and positions based on moving averages.
"""

import numpy as np
from config import Fast_MA, Slow_MA

def generate_signals(df):
    """
    generate_signals - generates +1, 0, -1 signals based
    on Fast_MA and Slow_MA crossovers
    """
    df["Signal"] = 0
    
    df.loc[df[Fast_MA] > df[Slow_MA], "Signal"] = 1
    df.loc[df[Fast_MA] < df[Slow_MA], "Signal"] = -1
    
    return df

def add_position(df):
    """
    add_position - adds the position depending on the signal,
    carries position forward if no new signal
    """

    prev_position = 0
    positions = []
    
    for index, row in df.iterrows():
        
        if row["Signal"] == 1:
            current_position = 1
        
        elif row["Signal"] == -1:
            current_position = -1
        
        else:
            current_position = prev_position
        
        positions.append(current_position)
        prev_position = current_position
    
    df["Position"] = positions
    
    return df

