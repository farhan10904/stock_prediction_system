"""
Simulates backtesting based on signal and position data. 
Tracks trades, P&L, and win rate.

"""
from config import stop_loss, take_profit, risk_per_trade, fixed_fee, percentage_fee, slippage

def open_long_trade(row, balance, risk_per_trade):
    """
    opens a long trade
    """
    entry_price = row["Price"]
    entry_time = row["Timestamp"]
    
    trade_amount = balance * risk_per_trade
    quantity = trade_amount / entry_price
    
    return entry_price, entry_time, trade_amount, quantity

def open_short_trade(row, balance, risk_per_trade):
    """
    opens a short trade
    """
    short_entry_price = row["Price"]
    short_entry_time = row["Timestamp"]
    
    trade_amount = balance * risk_per_trade
    quantity = trade_amount / short_entry_price
    
    return short_entry_price, short_entry_time, trade_amount, quantity

def close_long_trade_sl_tp(
row,
entry_price,
entry_time,
slippage,
fixed_fee,
percentage_fee,
win_profit,
loss_profit,
trade_log,
prev_position,
long_trades,
total_trade,
balance,
quantity
    ):
    
    """
    closes the long trade, using SL/ TP
    """
    
    sell_price = row["Price"]

    actual_long_entry = entry_price * (1 + slippage)
    actual_long_exit = sell_price * (1 - slippage)
    
    fee = fixed_fee + percentage_fee * (entry_price + sell_price)
    profit = (actual_long_exit - actual_long_entry) * quantity - fee
    
    cost_threshold =  (
        (entry_price + sell_price) * slippage +
        fixed_fee + percentage_fee * (entry_price + sell_price)
    )

    #if abs(profit) < cost_threshold :
        #return balance, long_trades, total_trade

    balance += profit

    if profit > 0:
        win_profit.append(profit)
    
    if profit < 0:
        loss_profit.append(profit)

    total_trade += 1
    long_trades += 1
    
    trade_info = {
        "Symbol": row["Symbol"],
        "Entry Price": entry_price,
        "Entry Time": entry_time,
        "Exit Time": row["Timestamp"],
        "Exit Price": row["Price"],
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
    }
    trade_log.append(trade_info)

    return balance, long_trades, total_trade

def close_long_trade_signal(
    row,
    entry_price,
    entry_time,
    slippage,
    fixed_fee,
    percentage_fee,
    win_profit,
    loss_profit,
    trade_log,
    prev_position,
    long_trades,
    total_trade,
    balance,
    quantity
    ):
    
    """
    closes the long trade, using signals
    """

    sell_price = row["Price"]
                
    actual_long_entry = entry_price * (1 + slippage)
    actual_long_exit = sell_price * (1 - slippage)
    
    fee = fixed_fee + percentage_fee * (entry_price + sell_price)
    profit = (actual_long_exit - actual_long_entry) * quantity - fee
    
    cost_threshold =  (
        (entry_price + sell_price) * slippage +
        fixed_fee + percentage_fee * (entry_price + sell_price)
    )

    #if abs(profit) < cost_threshold :
     #   return balance, long_trades, total_trade
    
    balance+= profit
    
    if profit > 0:
        win_profit.append(profit)
    
    if profit < 0:
        loss_profit.append(profit)

    total_trade += 1
    long_trades += 1
    
    trade_info = {
        "Symbol": row["Symbol"],
        "Entry Price": entry_price,
        "Entry Time": entry_time,
        "Exit Time": row["Timestamp"],
        "Exit Price": row["Price"],
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
    }
    
    trade_log.append(trade_info)
    
    return balance, long_trades, total_trade
    
def close_short_trade_sl_tp(
row,
short_entry_price,
short_entry_time,
slippage,
fixed_fee,
percentage_fee,
win_profit,
loss_profit,
trade_log,
prev_position,
short_trades,
total_trade,
balance,
quantity
    ):
    
    """
    closes the short trade, using SL/ TP
    """
    
    short_exit_price = row["Price"]
   
    actual_short_entry = short_entry_price * (1 + slippage)
    actual_short_exit =  short_exit_price * (1 + slippage)
    
    fee = fixed_fee + percentage_fee * (short_entry_price + short_exit_price)
    profit = (actual_short_entry - actual_short_exit) * quantity - fee
    
    cost_threshold =  (
        (short_entry_price + short_exit_price) * slippage +
        fixed_fee + percentage_fee * (short_entry_price + short_exit_price)
    )

  #  if abs(profit) < cost_threshold :
   #     return balance, short_trades, total_trade
    
    balance += profit
    
    if profit > 0:
        win_profit.append(profit)
    
    if profit < 0:
        loss_profit.append(profit)
    
    total_trade += 1
    short_trades += 1

    trade_info = {
        "Symbol": row["Symbol"],
        "Entry Price": short_entry_price,
        "Entry Time": short_entry_time,
        "Exit Time": row["Timestamp"],
        "Exit Price": row["Price"],
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
    }
    trade_log.append(trade_info)
    
    return balance, short_trades, total_trade

def close_short_trade_signal(
row,
short_entry_price,
short_entry_time,
slippage,
fixed_fee,
percentage_fee,
win_profit,
loss_profit,
trade_log,
prev_position,
short_trades,
total_trade,
balance,
quantity
):
    short_exit_price = row["Price"]
            
    actual_short_entry = short_entry_price * (1 + slippage)
    actual_short_exit =  short_exit_price * (1 + slippage)
    
    fee = fixed_fee + percentage_fee * (short_entry_price + short_exit_price)
    profit = (actual_short_entry - actual_short_exit) * quantity - fee
    
    cost_threshold =  (
        (short_entry_price + short_exit_price) * slippage +
        fixed_fee + percentage_fee * (short_entry_price + short_exit_price)
    )

  #  if abs(profit) < cost_threshold :
  #     return balance, short_trades, total_trade

    balance += profit
    
    if profit > 0:
        win_profit.append(profit)
    
    if profit < 0:
        loss_profit.append(profit)
    
    total_trade += 1
    short_trades += 1
    
    trade_info = {
        "Symbol": row["Symbol"],
        "Entry Price": short_entry_price,
        "Entry Time": short_entry_time,
        "Exit Time": row["Timestamp"],
        "Exit Price": row["Price"],
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
    }
    trade_log.append(trade_info)
    return balance, short_trades, total_trade

def close_remaining_long_trade(
    df,entry_price, entry_time, slippage, fixed_fee, 
    percentage_fee, win_profit, loss_profit, trade_log, 
    prev_position, long_trades, total_trade, balance,
    quantity       
):
    last_row = df
    last_price = last_row["Price"]
    last_time = last_row["Timestamp"]
    last_symbol = last_row["Symbol"]

    last_long_entry = entry_price * (1 + slippage)
    last_long_exit = last_price * (1 - slippage)
    
    fee = fixed_fee + (percentage_fee * entry_price)
    profit = (last_long_exit - last_long_entry) * quantity - fee
    
    balance += profit
    
    if profit > 0:
        win_profit.append(profit)

    if profit < 0:
        loss_profit.append(profit)

    total_trade += 1
    long_trades += 1
    
    trade_info = {
        "Symbol": last_symbol,
        "Entry Price": entry_price,
        "Entry Time": entry_time,
        "Exit Time": last_time,
        "Exit Price": last_price,
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
        }
    trade_log.append(trade_info)
    return balance, long_trades, total_trade
    
def close_remaining_short_trade(
    last_row, short_entry_price, short_entry_time, slippage, fixed_fee, 
    percentage_fee, win_profit, loss_profit, trade_log, 
    prev_position, short_trades, total_trade, balance,
    quantity
):
    last_price = last_row["Price"]
    last_symbol = last_row["Symbol"]
    last_time = last_row["Timestamp"]

    last_short_entry = short_entry_price * (1 + slippage)
    last_short_exit = last_price * (1 + slippage)

    fee = fixed_fee + (percentage_fee * short_entry_price)
    profit = (last_short_entry - last_short_exit) * quantity - fee

    balance += profit

    if profit > 0:
        win_profit.append(profit)

    if profit < 0:
        loss_profit.append(profit)

    total_trade += 1
    short_trades += 1

    trade_info = {
        "Symbol": last_symbol,
        "Entry Price": short_entry_price,
        "Entry Time": short_entry_time,
        "Exit Time": last_time,
        "Exit Price": last_price,
        "Closed Position": prev_position,
        "Profit": round(profit, 2)
    }
    trade_log.append(trade_info)
    return balance, short_trades, total_trade

def backtest_signals(df, balance):

    """
    Backtests trading performance based on a DataFrame 
    with 'Price' and 'Position' columns.

    Simulates trade entries and exits based on changes 
    in position:
    - Opens a long position when Position changes to 1
    - Opens a short position when Position changes to -1
    - Closes the trade when Position changes from 1 or -1 
    to something else

    Tracks:
    - Total profit
    - Win rate
    - Number of long and short trades
    - Detailed trade log (entry/exit, direction, profit)
    
    Returns:
    - results (dict): Summary statistics
    - trade_log (list of dicts): Detailed record of all trades
    
    """

    total_money = 0
    total_trade = 0
    prev_position = 0
    entry_price = 0
    short_entry_price = 0
    long_trades = 0
    short_trades = 0
    entry_time = None
    short_entry_time = None

    trade_log = []
    win_profit = []
    loss_profit = []

    #print(df["Position"].value_counts())

    for index, row in df.iterrows():
        #if prev_position != row["Position"]:
            #print(f"Transition at {row['Timestamp']}: {prev_position} -> {row['Position']}")
        # --- Long Trade --- # 
        if prev_position == 1 and entry_time is not None:
            pct_change = (row["Price"] - entry_price) / entry_price
            
            if pct_change <= stop_loss or pct_change >= take_profit:
            
                balance, long_trades, total_trade = close_long_trade_sl_tp(
                row, entry_price, entry_time, slippage, fixed_fee, 
                percentage_fee, win_profit, loss_profit, trade_log, 
                prev_position, long_trades, total_trade,
                balance, quantity
                )
                
                #prev_position = 0
                entry_price = 0
                entry_time = None
        
            elif row["Position"] != 1:

                balance, long_trades, total_trade = close_long_trade_signal(
                row, entry_price, entry_time, slippage, fixed_fee, 
                percentage_fee, win_profit, loss_profit, trade_log, 
                prev_position, long_trades, total_trade, balance, quantity)

                #prev_position = 0
                entry_price = 0
                entry_time = None
            
        # --- Short Trade: SL/TP --- # 
        if prev_position == -1 and short_entry_time is not None:
            pct_change = (short_entry_price - row["Price"]) / short_entry_price
    
            if pct_change <= stop_loss or pct_change >= take_profit:
                balance, short_trades, total_trade = close_short_trade_sl_tp(
                row, short_entry_price, short_entry_time, 
                slippage, fixed_fee, percentage_fee, win_profit,
                loss_profit, trade_log, prev_position, short_trades, 
                total_trade, balance, quantity)
                
                # Closes trade
                #prev_position = 0
                short_entry_price = 0
                short_entry_time = None

            elif row["Position"] !=-1:

                balance, short_trades, total_trade = close_short_trade_signal(
                row, short_entry_price, short_entry_time, slippage, 
                fixed_fee, percentage_fee, win_profit, 
                loss_profit, trade_log, prev_position, 
                short_trades, total_trade, balance, quantity) 
                
                #prev_position = 0
                short_entry_price = 0
                short_entry_time = None

        # --- 2. Open new position if needed ---
        #--- Open new Long---
        if row["Position"] == 1 and prev_position != 1:
            entry_price, entry_time, trade_amount, quantity = open_long_trade(row, balance, risk_per_trade)
          
        #--- Open new Short ---
        if row["Position"] == -1 and prev_position != -1:
            short_entry_price, short_entry_time, trade_amount, quantity = open_short_trade(row, balance, risk_per_trade)

        prev_position = row["Position"]

    if prev_position == 1 or prev_position == -1:
        last_row = df.iloc[-1]
        
        #close remaining long trade
        if prev_position == 1 and entry_time is not None: #long
            balance, long_trades, total_trade = close_remaining_long_trade(
                last_row, entry_price, entry_time, slippage, fixed_fee, 
                percentage_fee, win_profit, loss_profit, trade_log, 
                prev_position, long_trades, total_trade, balance, quantity) 

        #close remaining short trade         
        if prev_position == -1 and short_entry_time is not None: #short
            balance, short_trades, total_trade = close_remaining_short_trade(
                last_row, short_entry_price, short_entry_time, slippage, fixed_fee, 
                percentage_fee, win_profit, loss_profit, trade_log, 
                prev_position, short_trades, total_trade, quantity, balance) 
    
                   
    num_wins = len(win_profit)
    num_losses = len(loss_profit)
    total_trade = num_wins + num_losses
    
    wr = num_wins / total_trade if total_trade >0 else 0
    average_win = sum(win_profit) / num_wins if num_wins > 0 else 0
    average_loss = abs(sum(loss_profit)) / num_losses if num_losses > 0 else 0
    
    expectancy = wr * average_win - (1- wr) * average_loss

    results = {
        "Total Trades": total_trade,
        "Win Rate": wr*100,
        "Wins": num_wins,
        "Average Win": average_win,
        "Losses": num_losses,
        "Average Loss": average_loss,
        "expectancy": round(expectancy, 2),
        "Total Profit": round(balance, 2),
        "Long Trades": long_trades,
        "Short Trades": short_trades
    }

    return results, trade_log


