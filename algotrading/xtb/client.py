from http import server
import json
import asyncio
import logging
import datetime
import os
import pandas as pd

from datetime import datetime
from algotrading.xtb.xapi import xapi, exceptions
from algotrading.xtb.xapi.records import *
from algotrading.xtb.xapi.enums import TimeInt, PeriodCode, TradeDay
from algotrading.constants import *

# time = [TimeInt[time] for time in TimeInt.__dict__ if not str(time).startswith('_')][0]


class Client:
    """Client object for handling XTB websockets. """
    
    def __init__(self, account_id:int, password:str, symbol:str = "GBPJPY"):
        """Establish a client connection to XTB trading platform. 

        Args:
            account_id (int): _description_
            password (str): _description_
            backtesting (bool, optional): _description_. Defaults to False.
            symbol (str, optional): _description_. Defaults to "GBPJPY".
            ### timeframe (_type_, optional): The timeframe to get candle stick data on in stream. Defaults to PeriodCode.PERIOD_M15.
        """
        
        self.isDataRedundant = True
        self.symbol = symbol
        self.logger = logging.getLogger(__class__.__name__)
        self.disconnected = False
        
        self._logger_message = None
        
        self.credentials = {
            "accountId":account_id,
            "password":password,
            "host": "ws.xtb.com",
            "type": "demo",
            "safe": False
        }
        
        self._last_symbol = None # The previous lagging symbol data
        
            
        logging.basicConfig(
            format=f"{__class__.__name__}[{self.credentials['host']}] %(asctime)s >>> %(message)s",
            level=logging.INFO,
        )
        
    def get_local_time(self) -> datetime:
        """ Get the current time in string format of DD/MM/YY H/M/S. """
        
        time = datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S%f')
        time = datetime.datetime.strptime(time, '%d/%m/%Y %H:%M:%S%f')
        return time
    
    def to_milliseconds(self, days:int = 0, hours:int = 0, minutes:int = 0) -> int:
        """ Return days, hours, or seconds in milliseconds. """
        
        milliseconds = (days*24*60*60*1000)+(hours*60*60*1000)+(minutes*60*1000)
        return milliseconds
        
    async def get_symbol(self, connector:xapi.XAPI, symbol:str) -> SymbolRecord:
        """ Returns a mapped 'SymbolRecord' version of symbol record data from connector.socket.getSymbol to output.

        Args:
            xapi_connector (xapi.XAPI): The async context manager API connector.
            symbol (str): The symbol to get a Symbol Record for.
        """
        new_symbol = await connector.socket.getSymbol(symbol)
        new_symbol_record = SymbolRecord(**new_symbol['returnData'])
        
        ## Get the previous symbol before the next and prevent duplicate times.
        if self._last_symbol is None:
            self._last_symbol = new_symbol_record
            return self._last_symbol
        elif self._last_symbol.time != new_symbol_record.time:
            self._last_symbol = new_symbol_record
            return self._last_symbol
        return
        
    async def get_tick_price(self, connector:xapi.XAPI, symbol:str) -> StreamTickRecord:
        """ Get new tick price data for a symbol on the stream.
        
        Args:
            connector (XAPI): the asynchronous context manager.
            symbol (str): The symbol to get a Tick Record for.
        """
        
        tick_price = await connector.stream.getTickPrices(symbol, maxLevel=6)
        # tick_price_record = TickRecord(**tick_price.get('data'))
        return tick_price
        
    async def get_last_request_data(self, connector:xapi.XAPI, symbol:str, period:PeriodCode, multiplier:int, timeframe:TimeInt = str) -> RateInfoRecord:
        """Get access to historical data over a timeframe and from a historical date.

        Args:
            connector (XAPI): the asynchronous context manager.
            symbol (str): The symbol to last request data for.
            period (PeriodCode): The intraday chart period or period code.
            multiplier (int): The amount of 'timeframe' to get historical data from.
            timeframe (TimeInt) = str: The TimeInt timeframe.
        """

        ## Create a start time to get historical data for
        timeframeStartMultiplier = multiplier
        start = 1000 * round(datetime.datetime.now().timestamp()) - (TimeInt[timeframe] * timeframeStartMultiplier)
        data = await connector.socket.getChartLastRequest(symbol, start, period)
        data = data.get('returnData')
        try:
            return [RateInfoRecord(**info) for info in data.get('rateInfos')] 
        except AttributeError:
            self.logger.info("The params parsed cannot return the data you asked for. Try changing the period, multiplier or timeframe.") 
    
    
    def __get_latest_file(self, path:str = None):
        """Get the latest file in a directory. Due to this being a client for trading it defaults to the backtesting data directory.

        Args:
            path (str, optional): The path to get the latest file from. Defaults to backtesting data path if None.

        Returns:
            dict: The 'latest' file information metadata.
        """
        ## Sets the latest backtest to latest.csv and updates the previous to the file date.
        if path is None:
            file_path = f"{os.getcwd()}\\algotrading\\backtest_data\\"
        else:
            file_path = path
        
        most_recent_file:str = None
        most_recent_time = 0
        for file in os.scandir(file_path):
            if file.is_file():
                creation_time = file.stat().st_ctime
                if creation_time > most_recent_time:
                    most_recent_file = file.name
                    most_recent_time = creation_time
        return {"file_name": most_recent_file, "creation_time": most_recent_time}
        
    def write_backtest_ohlcv_data(self, historical_data):
        """Write OHLCV historical data to a comma seperated values file. """

        if GET_NEW_HISTORICAL_DATA == True:
            file_path = f"{os.getcwd()}\\algotrading\\backtest_data\\"
            file_name = "latest.csv"
            latest_file = self.__get_latest_file()
            latest_file_name = latest_file['file_name']
            latest_file_time = latest_file['creation_time']
            
            if BACKTESTING == True:
                if latest_file_name == file_name:
                    ## Update old 'latest.csv' file to creation date.
                    latest_file_time = datetime.datetime.fromtimestamp(latest_file_time).strftime("%d.%m.%Y - %H.%M.%S")
                    new_file_name = f"{self.symbol} {PeriodCode(TRADE_PERIOD).name} {latest_file_time}.csv"
                    os.rename(file_path+latest_file_name, file_path+new_file_name)

                    ## Write new data to latest.csv file
                    try:
                        df = pd.DataFrame(historical_data)
                        df = df[['ctmString', 'ctm', 'open', 'high', 'low', 'close', 'vol']]
                        df.to_csv(file_path + file_name, index=False)
                    except KeyError:
                        return
                
                ## If latest_file_name is not file_name or no latest.csv found then make the latest the file.
                if latest_file_name != file_name:
                    if not os.path.isfile(file_path+file_name):
                        ## If no file exists then create an empty instance of latest.csv.
                        try:
                            df = pd.DataFrame(historical_data)
                            df = df[['ctmString', 'ctm', 'open', 'high', 'low', 'close', 'vol']]
                            df.to_csv(file_path + file_name, index=False)
                        except KeyError:
                            return
                            
                try:
                    os.rename(file_path+latest_file_name, file_path+file_name)
                except TypeError:
                    return
            else:
                ## Unlikely to throw due to pre-determined checks but if it does, no file writing can be invoked because backtesting is false.
                self.logger.info(f"You cannot write historical data to a file because BACKTESTING is set to {BACKTESTING}.")
            
            return
        
    async def get_backtest_ohlcv_data(self) -> pd.DataFrame:
        """ Async function of getting ohlcv data from file. We need to coroutine this to make sure all data is accounted for appropriately. """
        
        file = self.__get_latest_file()
        file_path = f"{os.getcwd()}\\algotrading\\backtest_data\\"
        file_name = file['file_name']
        file = pd.read_csv(file_path+file_name)
        df = file
        df = df.rename(columns={
            'open' : 'Open',
            'high' : 'High',
            'low' : 'Low',
            'close' : 'Close',
            'vol' : 'Volume'
            })
        
        ## Pre-process the data before returning a dataframe.
        df = df.drop(['ctm'], axis=1)
        df['ctmString'] = pd.to_datetime(df['ctmString'], format='%b %d, %Y, %I:%M:%S %p')
        df['Date'] = df['ctmString'].dt.date
        df['Date'] = pd.to_datetime(df['Date'])
        df['Time'] = df['ctmString'].dt.time
        df.drop(columns={'ctmString'}, inplace=True)
        df.set_index('Date', inplace=True)
        df.insert(0, 'Time', df.pop('Time'))
        
        ## Calculate the actual prices for Open, High, Low, Close.
        df['High'] = (df['Open'] + (df['High']))/1000
        df['Low'] = (df['Open'] + (df['Low']))/1000
        df['Close'] = (df['Open'] + (df['Close']))/1000
        df['Open'] = (df['Open'])/1000
        return df
    
    
    async def get_candles(self, connector:xapi.XAPI, symbol:str) -> StreamingCandleRecord:
        """ Subscribes for and unsubscribes from API chart candles. The interval of every candle is 1 minute. A new candle arrives every minute. """
        
        await connector.stream.getCandles(symbol)
        
    async def _get_trade_day(self, connector:xapi.XAPI):
        """Return trade day of server time as integer of week. """
        server_time = await connector.socket.getServerTime()
        epoch_time = int(str(server_time.get('returnData')['time'])[:-3]) # removed milliseconds.
        trade_day = datetime.datetime.fromtimestamp(epoch_time).isoweekday()
        return trade_day
        
    async def get_server_day(self, connector:xapi.XAPI) -> TradeDay:
        """Returns datetime.isoweekday as a dictionary of TradeDay. """
        trade_day = await self._get_trade_day(connector)
        trade_day = TradeDay(trade_day)
        return {'day': trade_day.value, 'description': trade_day.name}
    
    async def get_client_day(self, connector:xapi.XAPI):
        """Returns the difference in time between the server and the client's local time."""
        local_time = self.get_local_time()
        
        
    async def is_market_open(self, connector:xapi.XAPI, symbol:str) -> bool:
        """Returns a boolean of the market being open on the day this function is executed.
        
                
        Args:
            connector (XAPI): the asynchronous context manager.
            symbol (str): The market symbol to check for.
            verbose (bool): Enable extra market information to output to logger.
        
        For simplicity we are going to assume markets that do not open from time 0 are considered not open even in reality they might be for short periods of time.
        
        - Its important to note that 'Candle start time is in CET / CEST time zone (see Daylight Saving Time, DST)'.
        - This means that we have to account for time differences.
        
        ## Example:
            - {'status': True, 'returnData': 
            - [{'symbol': 'GBPJPY', 'trading': [
            - {'day': 7, 'fromT': 82800000, 'toT': 86400000}, 
            - {'day': 1, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 5, 'fromT': 0, 'toT': 79200000}, 
            - {'day': 3, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 4, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 2, 'fromT': 0, 'toT': 86400000}], s
            - 'quotes': [
            - {'day': 4, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 1, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 3, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 2, 'fromT': 0, 'toT': 86400000}, 
            - {'day': 7, 'fromT': 82800000, 'toT': 86400000},
            - {'day': 5, 'fromT': 0, 'toT': 79200000}
            - ]},
            
            You can see that the market on day 7 (Sunday) is open but not for long which is why a live algorithm would be useless to implement on that particular day.
        """
        
        server_day = await self.get_server_day(connector)
        trading_hours = await connector.socket.getTradingHours(symbol)
        
        server_time = await connector.socket.getServerTime()
        epoch_time = int(str(server_time.get('returnData')['time'])[:-3])
        server_intraday_hour = datetime.datetime.fromtimestamp(epoch_time).hour
        
        #if ((server_intraday_hour >= MIN_TRADING_INTRADAY_HOUR) and (server_intraday_hour <= MAX_TRADING_INTRADAY_HOUR)) or (BACKTESTING == True)
        # removed backtesting because if trading in forwards time backtesting is not a required param.
        if ((server_intraday_hour >= MIN_TRADING_INTRADAY_HOUR) and (server_intraday_hour <= MAX_TRADING_INTRADAY_HOUR)):
            for i in range(len(trading_hours.trading)):
                trading_record = TradingRecord(**trading_hours.trading[i])
                if server_day['day'] == trading_record.day:
                    max_trading_intraday_hour = int(trading_record.toT/1000/60/60 - 1)
                    
                    ## Remaining trading hours left until rollover fees. From 23 to 0 then resets.
                    rollover_occurance = max_trading_intraday_hour - server_intraday_hour
                    if rollover_occurance == 0:
                        ## Prevent NEW trades from being rolled over. This does not prevent active trades from accumulating fees.
                        self.logger.info(f"Sorry I cannot allow trades to accumulate rollover fees. ¯\_(ツ)_/¯")
                        return False
                    
                    if VERBOSE:
                        self.logger.info(f"Trading {self.symbol} between hours {MIN_TRADING_INTRADAY_HOUR} and {MAX_TRADING_INTRADAY_HOUR}")
                    return True
        else:
            ## Server time is either above or below our constant range limit so make new checks.
            if OVERRIDE_TRADING_INTRADAY_RANGE:
                for i in range(len(trading_hours.trading)):
                    trading_record = TradingRecord(**trading_hours.trading[i])
                    if server_day['day'] == trading_record.day:
                        
                        ## Format the trading intraday max hour
                        ## We have to minus an hour due to datetime epoch hour starting at 0.
                        max_trading_intraday_hour = int(trading_record.toT/1000/60/60 - 1)
                        
                        ## Remaining trading hours left until rollover fees. From 23 to 0 then resets.
                        rollover_occurance = max_trading_intraday_hour - server_intraday_hour
                        if rollover_occurance == 0:
                            ## Prevent NEW trades from being rolled over. This does not prevent active trades from accumulating fees.
                            self.logger.info(f"Sorry I cannot allow trades to accumulate rollover fees. ¯\_(ツ)_/¯")
                            return False
                        
                        ## Check if trading is still allowed below our max trading intraday hour.
                        if server_intraday_hour < max_trading_intraday_hour:
                            if VERBOSE:
                                self.logger.info(f"OVERRIDE_TRADING_INTRADAY_RANGE has been enabled for {self.symbol}. FBI will be at your door soon. ¯\_(ツ)_/¯")
                            return True
                        
        return False
        
        
    
    
    # async def run(self, **args):
    #     """Run an websocket client instance and connect to a XTB URL.
        
    #     Args:
    #         args (Any): The different functions to parse into the client websocket.
    #     """
        
    #     logging.basicConfig(
    #         format=f"{__class__.__name__}[{self.credentials['host']}] %(asctime)s >>> %(message)s",
    #         level=logging.INFO,
    #     )
        
    #     if not BACKTESTING:
        
    #         while not self.disconnected:
    #             try:
    #                 async with await xapi.connect(**self.credentials) as api:
    #                     # candle = await self.get_candles(api, "GBPJPY", PeriodCode.PERIOD_M1)
    #                     # print(candle)
    #                     # break
                        
    #                     # candle = await api.stream.getCandles('GBPJPY')
            
    #                     # if candle is not None:
    #                     #     print(candle)
    #                     # await api.stream.stopCandles('GBPJPY')
                        
    #                     await self.get_candles(api, self.symbol)
                        
    #                     async for message in api.stream.listen():
    #                         self.logger.info(message)
                        
                        
    #             except exceptions.LoginFailed as e:
    #                 print(f"Log in failed: {e}")
    #                 self.disconnected = True
                        
    #             except exceptions.ConnectionClosed as e:
    #                 print(f"Connection closed: {e}, reconnecting ...")
    #                 await asyncio.sleep(1)
    #                 continue
                
                
    #             ## Catch any NoneTypes and continue
    #             # except AttributeError as e:
    #             #     continue
        
        
    #     if BACKTESTING:
    #         """
            
    #             If backtesting is enabled then the account will be a demo account on XTB for security purposes.
    #             We want to get historical data over a period of time and calculate strategy rate over intraday timeframes.
                
    #             TO DO LIST:
    #             - Write new historical data to file/Data frame.
    #             - Read the data from backtest location
    #             - Apply the indicators to the data
    #             - Use the algorithms ontop of that to determine buy and sell signals (Breakout trading).
            
    #         """
            
    #         try:
    #             async with await xapi.connect(**self.credentials) as api:
                    
    #                 last_chart_record = await self.get_last_request_data(
    #                     connector=api,
    #                     symbol="GBPJPY",
    #                     period=PeriodCode.PERIOD_D1,
    #                     multiplier=10,
    #                     timeframe='YEARS'
    #                 )
                        
    #                 if self.isDataRedundant == True:
    #                     ## Write last_chart_request to file
    #                     dt = datetime.datetime.now()
    #                     df = pd.DataFrame(last_chart_record)
    #                     df = df[['ctmString', 'ctm', 'open', 'high', 'low', 'close', 'vol']]
    #                     # print(df)
    #                     df.to_csv(f"{os.getcwd()}\\algotrading\\backtest_data\\backtest_{self.symbol} - {dt.day}.{dt.month}.{dt.year} - {dt.hour}.{dt.minute}.{dt.second}.csv", index=False)
                    
    #         except exceptions.ConnectionClosed as e:
    #             print(f"Connection closed: {e}, reconnecting ...")
    #             await asyncio.sleep(1)
                
    #         except exceptions.LoginFailed as e:
    #             print(f"Log in failed: {e}")
    
    
    
    
    
    
    
    
    
              
    
    # async def get_candles(self, connector:xapi.XAPI, symbol, period:PeriodCode) -> RateInfoRecord:
    #     ## If period > 1 minute calculate X minutes for that period code to return data.
        
    #     time = await connector.socket.getServerTime()
    #     start = time.get('returnData')['time']
        
    #     match (period):
    #         case PeriodCode.PERIOD_M1:
    #             start = start - 21690000
        
    #     candle = await connector.socket.getChartLastRequest(symbol, start, period)
    #     return candle