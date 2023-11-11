import os
import pandas as pd



class _Backtesting:
    """
    Base class for our backtesting.
    Contains class variables about our testing and data/file handling.
    """
    
    def get_historical_data(self, file_name:str = None) -> pd.DataFrame:
        
        # if None use api data
        if file_name is None: return
        
    def get_period_data(self, period:dict | int):
        """Gets historical data from a set of candle periods.

        Args:
            period (dict | int): The amount of candles for a given range to the newest indication.
        """
    
    

class Backtesting(_Backtesting):
    """
    We need to backtest to find out details about our strategy.
    This means getting historical data first and then using our strategy on top.
    
    """
    
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.date_duration = None
        self.win_rate = None
        self.best_trade = None
        self.worst_trade = None
        self.sharpe_ratio = None
        
        ## we want to know the drawdown to find where large movements occur.
        
    def append_new_data(self):
        return
    
    def get_random_test_data(self) -> pd.DataFrame:
        """ Get random range of test data from backtesting historical data. """

    
    
