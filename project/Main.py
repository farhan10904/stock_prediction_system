"""
Main launcher
Choose function to run
"""
from config import symbols
from modules.runner import (
    run_predictor, 
    run_backtests, 
    prepare_analysis,
    export_all_trades, 
    get_all_historical_data,
    profit_summary)

if __name__ == "__main__":
    print("Select an action to run:")
    print("1. Run Predictor")
    print("2. Run Backtests")
    print("3. Prepare Analysis")
    print("4. Export All Trades")
    print("5. Get Historical Data")
    print("6. Show Profit Summary")

    choice = input("Enter 1 to 6: ")

    if choice == "1":
        run_predictor()
    elif choice == "2":
        run_backtests()
    elif choice == "3":
        prepare_analysis()
    elif choice == "4":
        export_all_trades()
    elif choice == "5":
        get_all_historical_data()
    elif choice == "6":
        profit_summary()
    #elif choice == "7":
        #
    else:
        print("Invalid choice.")

